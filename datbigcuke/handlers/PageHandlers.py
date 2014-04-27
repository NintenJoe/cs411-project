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
import urllib

import os
import datetime
from os.path import join as join_paths
from os.path import exists as file_exists
from datetime import datetime
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
        errors = {}
        if self.get_argument('unconfirmed', default=None) != None:
            errors['email'] = "You must validate your email."
        if self.get_argument('baduser', default=None) != None:
            errors['email'] = "Bad Email." 

        if self.get_argument('badpass', default=None) != None:
            errors['badpass'] = "Bad Password"

        if not self.get_current_user():
            self.render( self.get_url(), errors = errors )
        else:
            self.redirect( "/main" )


    ##  @override
    def post( self ):
        user_email = self.get_argument( "user_email" )
        user_password = self.get_argument( "user_password" )

        repo = UserRepository()
        user = repo.get_user_by_email(user_email)
        repo.close()
        params = {}
        if user is not None:
            # user exists. does the password match?
            if user.match_password(user_password):
                # password is correct. Has user confirmed their email?
                if user.confirmed:
                    self.set_current_user(user.id)
                else:
                    params["unconfirmed"] = True
                    self.redirect( "/?"  + urllib.urlencode(params) )
            else:
                params["badpass"] = True
                self.redirect( "/?"  + urllib.urlencode(params) )
        else:
            params["baduser"] = True
            self.redirect( "/?"  + urllib.urlencode(params) )

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
    @PageRequestHandler.page_title.getter
    def page_title( self ):
        return "Registration"

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

        # NOTE: The deadlines are assumed to be sorted by time.
        # TODO: Retrieve the deadlines associated with the user here.
        deadline_list = []

        # NOTE: The groups are assumed to be sorted alphabetically.
        # TODO: Retrieve the groups associated with the user here.
        group_list = []

        self.render( self.get_url(),
             user = user,
             deadlines = deadline_list,
             groups = group_list
        )

    ##  @override
    @PageRequestHandler.page_title.getter
    def page_title( self ):
        return "Main Page"

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
        user = self.get_current_user()

        # NOTE: The deadlines are assumed to be sorted by time.
        # TODO: Retrieve the deadlines associated with the user here.
        deadline_list = []

        # NOTE: The groups are assumed to be sorted alphabetically.
        # TODO: Retrieve the groups associated with the user here.
        group_list = []

        self.render( self.get_url(),
             user = user,
             groups = group_list
        )

    ##  @override
    @PageRequestHandler.page_title.getter
    def page_title( self ):
        return "Profile Page"

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
        self.render( self.get_url() )

    ##  @override
    @PageRequestHandler.page_title.getter
    def page_title( self ):
        return "Group Page"

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

##  Rendering module for the listing of deadlines associated with a particular
#   user and/or group.
class DeadlineListModule( WebModule ):
    ##  @override
    #
    #   @param deadline_list A listing of deadline entity objects.
    def render( self, deadline_list ):
        # TODO: Add pre-processing at this stage.
        note_example = "This is an example of a longer note.  It's long!"
        deadlines = [
            {
                "name": "Final Project",
                "group": "CS411",
                "time": datetime( 2014, 4, 27, 23, 59 ).strftime( "%A %B %m, %I:%M %p" ),
                "notes": note_example
            },
            {
                "name": "Final Project",
                "group": "CS467",
                "time": datetime( 2014, 5, 1, 9, 0, 0 ).strftime( "%A %B %m, %I:%M %p" ),
                "notes": note_example
            },
        ]
        for i in range(4):
            deadlines += deadlines

        return self.render_string( self.get_url(), deadlines = deadlines )

    ##  @override
    @WebResource.resource_url.getter
    def resource_url( self ):
        return "deadline-list.html"


##  Rendering module for the listing of members associated with a particular
#   course or group.
class MemberListModule( WebModule ):
    ##  @override
    #
    #   @param deadline_list A listing of user entity objects.
    def render( self, deadline_list ):
        # TODO: Add pre-processing at this stage.
        members = member_list

        return self.render_string( self.get_url(), members = members )

    ##  @override
    @WebResource.resource_url.getter
    def resource_url( self ):
        return "member-list.html"

##  Rendering module for a hierarchy of groups associated with a particular
#   user and/or group.
class GroupTreeModule( WebModule ):
    ##  @override
    #
    #   @param group_list A listing of group entity objects.
    def render( self, group_list ):
        # TODO: Add pre-processing at this stage.
        group_forest = [
            { "name": "CS411", "gid": 1, "maintainer": "Ryan Cunningham", "subgroups": [
                { "name": "DBC", "gid": 2, "maintainer": "Eunsoo Roh", "subgroups": [] },
                { "name": "Phuong", "gid": 3, "maintainer": "Phuong", "subgroups": [] },
            ] },
            { "name": "CS428", "gid": 4, "maintainer": "Darko Marinov", "subgroups": [
                { "name": "Cosmin", "gid": 5, "maintainer": "Cosmin", "subgroups": [] },
                { "name": "Zol", "gid": 6, "maintainer": "Joe Ciurej", "subgroups": [] },
            ] },
            { "name": "CS467", "gid": 7, "maintainer": "Karrie Karahalios", "subgroups": [
                { "name": "Team 2", "gid": 8, "maintainer": "Efe Karakus", "subgroups": [] },
            ] },
            { "name": "CS210", "gid": 8, "maintainer": "Alex Kirlik", "subgroups": [] },
        ]
        group_forest += group_forest

        return self.render_string( self.get_url(), group_forest = group_forest )

    ##  @override
    @WebResource.resource_url.getter
    def resource_url( self ):
        return "group-tree.html"


##  Rendering module for a listing of group trees (i.e. a group forest).  This
#   modules acts as a recursive helper rendering module for 'GroupTree' UI module.
class GroupForestModule( WebModule ):
    ##  @override
    #
    #   @param group_list A list of groups which contain their inner group
    #    information as nested lists (see 'GroupTreeModule').
    def render( self, group_forest ):
        return self.render_string( self.get_url(), level_groups = group_forest )

    ##  @override
    @WebResource.resource_url.getter
    def resource_url( self ):
        return "group-forest.html"

