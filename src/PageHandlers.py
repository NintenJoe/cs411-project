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
    ##  @override
    def get_url( self ):
        return join_paths( "html", self.resource_url )

    ##  @return True if the user is authenticated on the website and false
    #   otherwise.
    def is_user_authenticated( self ):
        return self.get_user_json() != None

    ##  @return The JSON object describing the user that's currently authenticated,
    #   or "None" if no such user exists.
    def get_user_json( self ):
        user_cookie = self.get_secure_cookie( self.cookie_name )
        return tornado.escape.json_decode( user_cookie ) if user_cookie else None

    ##  @return The name of the user that's currently authenticated, or "None" if
    #   no such user exists.
    def get_user_name( self ):
        user_json = self.get_user_json()
        return tornado.escape.xhtml_escape( user_json["name"] ) if user_json else None

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
        self.render( self.get_url() )

    ##  @override
    def post( self ):
        user_email = self.get_argument( "user_email" )
        user_password = self.get_argument( "user_password" )

        # TODO: Verify that the user name exists.
        pass

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
        user_name = self.get_user_name()
        # TODO: Fill in the courses for this user.
        user_courses = []

        self.render( self.get_url(), user=user_name, courses=user_courses )

    ##  @override
    @WebResource.resource_url.getter
    def resource_url( self ):
        return "user_profile.html"


##  Page handler for the "/edit" (user information editing) web page.
class UserEditHandler( PageHandler ):
    ##  @override
    @tornado.web.authenticated
    def get( self ):
        pass

    ##  @override
    def post( self ):
        pass

    ##  @override
    @WebResource.resource_url.getter
    def resource_url( self ):
        return "user_edit.html"


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
