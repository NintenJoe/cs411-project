##  @file AsyncHandlers.py
#   @author Joshua Halstead
#   @date Spring 2014
#
#   Cotainer module for all classes related to handling asynchronous requests
#   from clients.
#
#   @see http://stackoverflow.com/q/5902684
#   @see https://groups.google.com/forum/#!msg/python-tornado/-9EgFbOnDGs/8LgB1i9xFEgJ
#
#   @TODO
#   - Look into using the '@asynchronous' decorator to make these handlers
#     more asynchronous.

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


### Asynchronous Request Handlers ###

##  TODO: Write the implementation of this asynchronous handler.
class AsyncHandler( PageHandler ):
    ##  @override
    def post( self ):
        self.set_current_user( None )
        self.redirect( "/" )

