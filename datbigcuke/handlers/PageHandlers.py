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
from datbigcuke.entities import Deadline
from datbigcuke.entities import DeadlineRepository
from datbigcuke.cukemail import CukeMail


# TODO: Remove.
import hashlib
import urllib


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

        gr = GroupRepository()
        uiuc = gr.fetch_by_name("UIUC")
        if uiuc == []:
            g = Group()
            g.name = "UIUC"
            g.description = "University of Illinois at Urbana/Champaign"
            g.type = 0
            gr.persist(g)
            gr.close()
        uiuc = gr.fetch_by_name("UIUC")

        repo = UserRepository()
        user = repo.persist(user)
        user.groups = []
        repo.add_user_to_group(user, uiuc[0])
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
        gr = GroupRepository()
        dr = DeadlineRepository()

        user = self.get_current_user()
        root_group = gr.get_user_group_tree(user.id)
        gr.get_group_maintainer_rec(root_group)

        deadline_list = dr.deadlines_for_user(user.id)
        for deadline in deadline_list:
            deadline.group = gr.fetch(deadline.group_id)

        self.render( self.get_url(),
            user = user,
            deadlines = deadline_list,
            groups = [ root_group ]
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

        self.render( self.get_url(),
            user = user,
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
        ur = UserRepository()
        gr = GroupRepository()
        dr = DeadlineRepository()

        # TODO: 404 if the user is not a member of the group.
        user = self.get_current_user()
        # TODO: 404 if the page doesn not exist in the DB.
        group = gr.get_user_group_tree(user.id, long(group_id))
        gr.get_group_maintainer_rec(group)
        supergroup_list = gr.get_supergroup_list(group_id)

        group_is_public = group.maintainerId == None
        user_is_maintainer = group.maintainerId == user.id
        member_list = ur.get_members_of_group(group_id)

        # TODO: Add functionality to integrate the groups with the deadlines
        # to allow for front-end maintainer validation when modifying deadlines.
        deadline_list = dr.deadlines_for_user_for_group(user.id, group.id)
        for deadline in deadline_list:
            deadline.group = group

        self.render( self.get_url(),
            user = user,
            group = group,
            supergroups = supergroup_list,
            subgroups = group.subgroups,
            group_is_public = group_is_public,
            user_is_maintainer = user_is_maintainer,
            members = member_list,
            deadlines = deadline_list,
        )

    ##  @override
    @PageRequestHandler.page_title.getter
    def page_title( self ):
        return "Group Page"

    ##  @override
    @WebResource.resource_url.getter
    def resource_url( self ):
        return "group.html"


### Miscellaneous Handlers ###

##  Page handler for the "/group-leave" (user group leaving/deleting) web page.
class GroupLeaveHandler( PageRequestHandler ):
    ##  @override
    @tornado.web.authenticated
    def post( self, group_id ):
        ur = UserRepository()
        gr = GroupRepository()

        user = self.get_current_user()
        group = gr.fetch(group_id)
        gr.get_group_maintainer(group)

        user_group_ids = [ g.id for g in gr.get_groups_of_user(user.id) ]
        supergroups = gr.get_supergroup_list(group_id)

        # The group must be a non-root group to consider removal.
        if len(supergroups) != 0:
            supergroup = supergroups[-1]

            # Case 1: User requested group deletion (user is maintainer + empty).
            if group.maintainerId == user.id and gr.get_group_size(group.id) == 1:
                gr.remove(group)
                self.redirect( "/group/" + str(supergroup.id) )
                return
            # Case 2: User requested to leave the group (user is in group).
            if group.id in user_group_ids:
                user.groups = [ gid for gid in user_group_ids if gid != group.id ]
                ur.persist(user)
                self.redirect( "/group/" + str(supergroup.id) )
                return

        self.redirect( "/group/" + str(group_id) )


##  Page handler for the "/logout" (user logout) web page.
class LogoutHandler( PageRequestHandler ):
    ##  @override
    @tornado.web.authenticated
    def get( self ):
        self.set_current_user( None )
        self.redirect( "/" )


### UI Modules ###

##  A general type of UI module that renders a template UI module specified
#   by a given file with a given set of keyword arguments.
class RenderTemplateModule( tornado.web.UIModule ):
    ##  @override
    #
    #   @param template_name The name of the template HTML file.
    #   @param kwargs A listing of keyword arguments to be passed to the template.
    def render( self, template_name, **kwargs ):
        template_url = join_paths( "html", "modules", template_name + ".html" )

        return self.render_string( template_url, **kwargs )

##  Rendering module for basic input form modals.  This module supports the
#   rendering of a few different template modals with minor differences.
class SimpleModalModule( WebModule ):
    ##  @override
    #
    #   @param modal_type The type of modal given as a string.
    def render( self, modal_type ):
        modal_id = modal_type
        modal_title = None

        if modal_id == "add-member":
            modal_title = "Add a Group Member"
        elif modal_id == "add-subgroup":
            modal_title = "Add a Group Subgroup"
        elif modal_id == "add-course":
            modal_title = "Add a Course"
        elif modal_id == "add-deadline":
            modal_title = "Add a Group Deadline"

        return self.render_string( self.get_url(),
            modal_id = modal_type,
            modal_title = modal_title,
        )

    ##  @override
    @WebResource.resource_url.getter
    def resource_url( self ):
        return "modal.html"

