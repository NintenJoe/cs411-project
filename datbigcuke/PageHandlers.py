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

import os
from os.path import join as join_paths
from os.path import exists as file_exists

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

    ##  @return The identifying email address for the user currently logged
    #   into the website or "None" if no such user exists.
    def get_current_user( self ):
        return self.get_secure_cookie( self.cookie_name )

    ##  @param user_email The email address for the user to be logged into the
    #   website.  If this parameter is set the "None", the current user will
    #   be removed.
    def set_current_user( self, user_email ):
        if user_email:
            self.set_secure_cookie( self.cookie_name, user_email )
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

        # TODO: Verify that the user name exists.
        pass

        self.set_current_user( user_email )

        self.redirect( "/user" )

    ##  @override
    @WebResource.resource_url.getter
    def resource_url( self ):
        return "home.html"


##  Page handler for the "/register" (registration) web page.
class RegistrationHandler( PageHandler ):
    ##  @override
    def get( self ):
        self.render( self.get_url() )

    ##  @override
    def post( self ):
        user_email = self.get_argument( "user_email" )
        user_nickname = self.get_argument( "user_nickname" )
        user_password = self.get_argument( "user_password" )

        # TODO: Add this user to the database.
        pass

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
        user_email = self.get_current_user()
        # TODO: Retrieve nickname information based on email.
        user_nickname = user_email
        # TODO: Retrieve group information based on email.  Use the names of the
        # groups in this array.
        user_groups = []

        self.render( self.get_url(), user=user_nickname, groups=user_groups )

    ##  @override
    @WebResource.resource_url.getter
    def resource_url( self ):
        return "user_profile.html"


##  Page handler for the "/edit" (user information editing) web page.
class ProfileEditHandler( PageHandler ):
    ##  @override
    @tornado.web.authenticated
    def get( self ):
        user_email = self.get_current_user()
        # TODO: Retrieve nickname information based on email.
        user_nickname = user_email
        # Note: The information in the arrays below is sample data for front-end testing.
        # Please remove it when necessary.
        # TODO: Retrieve group information based on email.
        user_groups = [ "cgroup1", "cgroup2", "cgroup3" ]
        # TODO: Retrieve all available groups (prune groups that the user is in).
        available_groups = [ "group1", "group2", "group3" ]

        self.render( self.get_url(), user_email=user_email, user_nickname=user_nickname,
            user_groups=user_groups, available_groups=available_groups )

    ##  @override
    @tornado.web.authenticated
    def post( self ):
        user_email = self.get_current_user()

        # Note: These values will be empty strings if they shouldn't be updated.
        new_user_email = self.get_argument( "user_email" )
        new_user_nickname = self.get_argument( "user_nickname" )
        new_user_password = self.get_argument( "user_password" )

        # Note: This value will be a list of strings where each string is a group name.
        new_groups_string = self.get_argument( "new_user_groups" )
        new_user_groups = new_groups_string.split( "~" ) if new_groups_string else []
        new_user_groups = map( lambda s: s.encode( "ascii", "ignore" ), new_user_groups )

        # TODO: Update this user's information in the database.
        pass

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
