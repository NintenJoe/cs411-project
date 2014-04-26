##  @file PageHandlers.py
#   @author Joseph Ciurej
#   @date Winter 2014
#
#   Cotainer module for all classes related to handling web page requests
#   from clients.
#
#   @see https://github.com/facebook/tornado/blob/master/demos
#
#   @TODO
#   - Abstract the user interface module types to a different class module.

import tornado.web
import tornado.auth
import uuid

import os
from os.path import join as join_paths
from os.path import exists as file_exists
from datbigcuke.handlers.BaseHandlers import WebResource
from datbigcuke.handlers.BaseHandlers import WebModule
from datbigcuke.handlers.BaseHandlers import PageRequestHandler
from datbigcuke.entities import User
from datbigcuke.entities import UserRepository
from datbigcuke.entities import Group
from datbigcuke.entities import GroupRepository
from datbigcuke.cukemail import CukeMail


### User Login/Registration Handlers ###

##  Page handler for the "/" (home) web page, which facilitates user login.
class LoginHandler( PageRequestHandler ):
    ##  @override
    def get( self ):
        if not self.get_current_user():
            self.render( self.get_url() )
        else:
            self.redirect( "/main" )

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

        self.redirect( "/main" )

    ##  @override
    @WebResource.resource_url.getter
    def resource_url( self ):
        return "login.html"


##  Page handler for the "/register" (registration) web page.
class RegistrationHandler( PageRequestHandler ):
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


## Page handler for the "/verify" (verification) web page.
class VerifyHandler( PageRequestHandler ):
    ## @override
    def get(self, unique):
        repo = UserRepository()
        repo.mark_verified(unique)

        self.redirect("/")

    ##  @override
    @WebResource.resource_url.getter
    def resource_url( self ):
        return "verify.html"


### User Information Handlers ###

##  Page handler for the "/main" web page, which is the primary interface
#   for the user (main deadlines, group information, et cetera).
class UserMainHandler( PageRequestHandler ):
    ##  @override
    @tornado.web.authenticated
    def get( self ):
        user = self.get_current_user()

        self.render( self.get_url(), user=user.name )

    ##  @override
    @WebResource.resource_url.getter
    def resource_url( self ):
        return "main.html"


##  Page handler for the "/profile" web page, which displays the profile
#   information for the user (user information, group information, Gcalender).
class UserProfileHandler( PageRequestHandler ):
    ##  @override
    @tornado.web.authenticated
    def get( self ):
        self.render( self.get_url() )

    ##  @override
    @WebResource.resource_url.getter
    def resource_url( self ):
        return "profile.html"


##  Page handler for the "/group" web page, which contains all the information
#   for the user group being requested (i.e. i in "/group/i/").
class UserGroupHandler( PageRequestHandler ):
    ##  @override
    @tornado.web.authenticated
    def get( self, group_id ):
        print group_id
        self.render( self.get_url() )

    ##  @override
    @WebResource.resource_url.getter
    def resource_url( self ):
        return "group.html"


### Miscellaneous Handlers ###

##  Page handler for the "/logout" (user logout) web page.
class LogoutHandler( PageRequestHandler ):
    ##  @override
    @tornado.web.authenticated
    def get( self ):
        self.set_current_user( None )
        self.redirect( "/" )


### UI Modules ###

##  Rendering module for the summary segments for courses.
class CourseSummaryModule( WebModule ):
    ##  @override
    def render( self, course ):
        return self.render_string( self.get_url() )

    ##  @override
    def resource_url( self ):
        return "course_summary.html"

