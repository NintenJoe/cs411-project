##  @file PageHandlers.py
#   @author Joseph Ciurej
#   @date Winter 2014
#
#   Cotainer module for all classes related to handling web page requests
#   from clients (see https://github.com/facebook/tornado/blob/master/demos).
#
#   @TODO
#   - 

import tornado.web
import tornado.auth
import uuid

import os
from os.path import join as join_paths
from os.path import exists as file_exists
from datbigcuke.entities import User
from datbigcuke.entities import UserRepository
from datbigcuke.entities import Group
from datbigcuke.entities import GroupRepository
from datbigcuke.cukemail import CukeMail


### Helper Classes ###

##  An abstract base class for types that correspond to particular web
#   resources (typically HTML pages) on the file system.
class WebResource():
    ##  @return The full URL path of the resource corresponding to the
    #   type relative to the 'template_path' base path.
    def get_url( self ):
        return self.resource_url

    ##  @return The string that indicates the URL of the base resource
    #   relative to its containing directory (e.g. for '~/html/a.html', 
    #   pageURL is 'a.html').
    @property
    def resource_url( self ):
        return ".error.html"


### Page Handlers ###

##  The base page request handling type from which all page handlers for
#   the CS411 project web application extend.
class PageHandler( tornado.web.RequestHandler, WebResource ):
    ### User Handling Methods ###

    ##  @return The entities.User object for the user currently logged
    #   into the website or "None" if no such user exists.
    def get_current_user( self ):
        user_id_str = self.get_secure_cookie(self.cookie_name)
        if user_id_str is None:
            return None
        user_id = long(user_id_str)
        repo = UserRepository()
        user = repo.fetch(user_id)
        repo.close()
        return user

    ##  @param user_email The unique identifier for the user to be logged into
    #   the website.  If this parameter is set the "None", the current user will
    #   be removed.
    def set_current_user( self, user_id ):
        if user_id:
            self.set_secure_cookie( self.cookie_name, unicode(user_id) )
        else:
            self.clear_cookie( self.cookie_name )

    ### Page Resource Methods ###

    ##  @override
    def get_url( self ):
        return join_paths( "html", self.resource_url )

    ##  @return The string representing the title of the page being serviced
    #   by the instance handler.
    @property
    def page_title( self ):
        return "Official Website"

    ##  @return The string that identifies the cookie stored on the user's
    #   computer for identification.
    @property
    def cookie_name( self ):
        return "datbigcuke_user"


##  Page handler for the "/" (home) web page.
class HomeHandler( PageHandler ):
    ##  @override
    def get( self ):
        if not self.get_current_user():
            self.render( self.get_url() )
        else:
            self.redirect( "/user" )

    ##  @override
    def post( self ):
        user_email = self.get_argument( "user_email" )
        user_password = self.get_argument( "user_password" )

        repo = UserRepository()
        user = repo.get_user_by_email(user_email)
        repo.close()
        if user is not None:
            # user exists. does the password match?
            if user.match_password(user_password):
                # password is correct. Has user confirmed their email?
                if user.confirmed:
                    self.set_current_user(user.id)

        self.redirect( "/user" )

    ##  @override
    @WebResource.resource_url.getter
    def resource_url( self ):
        return "home.html"

## Page handler for the "/verify" (verification) web page.
class VerifyHandler( PageHandler ):
    
    ## @override
    def get(self, unique):
        repo = UserRepository()
        repo.mark_verified(unique)

        self.redirect("/")

    ##  @override
    @WebResource.resource_url.getter
    def resource_url( self ):
        return "verify.html"

##  Page handler for the "/register" (registration) web page.
class RegistrationHandler( PageHandler ):
    ##  @override
    def get( self ):
        self.render( self.get_url() )

    ##  @override
    def post( self ):
        unique = str(uuid.uuid4())
        
        user_email = self.get_argument( "user_email" )
        user_nickname = self.get_argument( "user_nickname" )
        user_password = self.get_argument( "user_password" )

        # add this user to the database.
        user = User()
        user.email = self.get_argument("user_email")
        user.name = self.get_argument("user_nickname")
        user.password = self.get_argument("user_password")
        user.confirmUUID = unique

        repo = UserRepository()
        repo.persist(user)
        repo.close()

        ## Send a verification email to the user
        m = CukeMail()
        m.send_verification(unique, user.email)

        self.redirect( "/" )

    ##  @override
    @WebResource.resource_url.getter
    def resource_url( self ):
        return "register.html"


##  Page handler for the "/user" (user profile) web page.
class UserProfileHandler( PageHandler ):
    ##  @override
    @tornado.web.authenticated
    def get( self ):
        user = self.get_current_user()
        g_repo = GroupRepository()
        all_groups = g_repo.fetch_all()
        user_groups = set(g_repo.get_groups_of_user(user.id))
        g_repo.close()

        self.render( self.get_url(), user=user.name, groups=user_groups )

    ##  @override
    @WebResource.resource_url.getter
    def resource_url( self ):
        return "user_profile.html"


##  Page handler for the "/edit" (user information editing) web page.
class ProfileEditHandler( PageHandler ):
    ##  @override
    @tornado.web.authenticated
    def get( self ):
        user = self.get_current_user()

        if not user:
            self.redirect( "/" )

        g_repo = GroupRepository()
        all_groups = g_repo.fetch_all()
        user_groups = set(g_repo.get_groups_of_user(user.id))
        user_group_ids = map(lambda g: g.id, user_groups)
        g_repo.close()
        available_groups = [g for g in all_groups if g.id not in user_group_ids]

        self.render( self.get_url(), user_email=user.email, user_nickname=user.name,
            user_groups=user_groups, available_groups=available_groups )

    ##  @override
    @tornado.web.authenticated
    def post( self ):
        user = self.get_current_user()

        # Note: These values will be empty strings if they shouldn't be updated.
        new_user_email = self.get_argument( "user_email" )
        new_user_nickname = self.get_argument( "user_nickname" )
        new_user_password = self.get_argument( "user_password" )

        # Note: This value will be a list of strings where each string is a group id.
        new_groups_string = self.get_argument( "new_user_groups" )
        new_user_groups = new_groups_string.split( "~" ) if new_groups_string else []
        new_user_groups = map( long, new_user_groups )

        user.groups = new_user_groups

        if new_user_email:
            user.email = new_user_email
        if new_user_nickname:
            user.name = new_user_nickname
        if new_user_password:
            user.password = new_user_password

        # TODO: improve error handling
        repo = UserRepository()
        repo.persist(user)
        repo.close()

        self.redirect( "/user" )

    ##  @override
    @WebResource.resource_url.getter
    def resource_url( self ):
        return "user_edit.html"


##  Page handler for the "/logout" (user logout) web page.
class LogoutHandler( PageHandler ):
    ##  @override
    @tornado.web.authenticated
    def get( self ):
        self.set_current_user( None )
        self.redirect( "/" )


### UI Modules ###

##  The base page HTML module type from which all module types for the CS411 
#   project web application extend.
class PageModule( tornado.web.UIModule, WebResource ):
    ##  @override
    def get_url( self ):
        return join_paths( "html", "modules", self.resource_url )


##  Rendering module for the summary segments for courses.
class CourseSummaryModule( PageModule ):
    ##  @override
    def render( self, course ):
        return self.render_string( self.get_url() )

    ##  @override
    def resource_url( self ):
        return "course_summary.html"

