##  @file AsyncHandlers.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Cotainer module for all base classes related to handling user requests.
#
#   @TODO
#   - Export the classes related to UI modules and resources to a different
#     class module.

import tornado.web

import os
from os.path import join as join_paths
from os.path import exists as file_exists
from datbigcuke.entities import User
from datbigcuke.entities import UserRepository
from datbigcuke.entities import Group
from datbigcuke.entities import GroupRepository


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


##  The base page HTML module type from which all module types for the CS411 
#   project web application extend.
class WebModule( tornado.web.UIModule, WebResource ):
    ##  @override
    def get_url( self ):
        return join_paths( "html", "modules", self.resource_url )


##  An abstract base type that represents all primary handlers (both synchronous
#   and asynchronous) implemented in the DatBigCuke back-end.
class WebRequestHandler( tornado.web.RequestHandler ):
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

    ### User Resource Methods ###

    ##  @return The string that identifies the cookie stored on the user's
    #   computer for identification.
    @property
    def cookie_name( self ):
        return "datbigcuke_user"


##  The base page request handling type, which serves as the base for all DBC
#   handlers that handle page-related requests.
class PageRequestHandler( WebRequestHandler, WebResource ):
    ##  @override
    def get_url( self ):
        return join_paths( "html", self.resource_url )

    ##  @return The string representing the title of the page being serviced
    #   by the instance handler.
    @property
    def page_title( self ):
        return "Official Website"


##  The base asynchronous request handling type, which serves as the base
#   for all DBC handlers that handle asynchronous (i.e. AJAX) requests.
class AsyncRequestHandler( WebRequestHandler ):

    @tornado.gen.coroutine
    @tornado.web.authenticated
    def post( self ):
        print "async handler"
        user = self.get_current_user()
        data = self.get_arguments("data", None)
        print data

        # 'Logged-in' user must be defined
        if not user:
            return

        # Data must be defined
        if not data:
            return

        if not self._valid_request(user, data):
            return

        yield self._perform_request(user, data)

    def _valid_request(self, user, data):
        raise Exception("AsyncRequestHandler._valid_request must be overriden.")
        pass

    def _perform_request(self, user, data):
        raise Exception("AsyncRequestHandler._update must be overriden.")
        pass

    def _persist_user(self, user):
        """Save any user changes to the database"""
        user_repo = UserRepository()
        user_repo.persist(user)
        user_repo.close()

    def _persist_group(self, group):
        """Save any group changes to the database"""
        group_repo = GroupRepository()
        group_repo.persist(group)
        group_repo.close()
