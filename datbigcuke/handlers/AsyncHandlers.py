""" Container module for asynchronous request handling classes.

@TODO(halstea2): Look into used the @asynchronous decorator
"""

__author__ = 'Joshua Halstead'
__copyright__ = 'Copyright 2014 Datbigcuke Project'
__email__ = 'halstea2@illinois.edu'

import tornado.web
import tornado.auth
import uuid
import datetime
import json

# For test async handler only
import tornado.httpclient

from datbigcuke.handlers.BaseHandlers import WebResource
from datbigcuke.handlers.BaseHandlers import WebModule
from datbigcuke.handlers.BaseHandlers import AsyncRequestHandler
from datbigcuke.entities import User
from datbigcuke.entities import UserRepository
from datbigcuke.entities import Group
from datbigcuke.entities import GroupRepository
from datbigcuke.cukemail import CukeMail


# @TODO(halstea2) sanitize user data??
# @TODO(halstea2) Require authentication for all via @tornado.web.authenticated

class TestHandler(AsyncRequestHandler):
    @tornado.gen.coroutine
    @tornado.web.authenticated
    def post(self):
        data = self.get_argument("data", default=None)
        if not data:
            print str(datetime.datetime.now()) + " Received: None"
            self.write(json.dumps({"date": str(datetime.datetime.now()),
                                   "Status": 404}))

        print str(datetime.datetime.now()) + " Received: " +\
              str(json.dumps(data,
                             sort_keys=True,
                             indent=4,
                             separators=(',', ': ')
                 )
        )

        http_client = tornado.httpclient.AsyncHTTPClient()
        response = yield http_client.fetch("http://google.com")
        self.write(json.dumps({"date": str(datetime.datetime.now()),
                               "response": str(response)}))
# ../group/[id]
# Required Handlers

class LeaveGroupHandler(AsyncRequestHandler):
    """Async Handler for leaving a group"""

    def _valid_request(self, user, data):
        """Verify that the 'leave group' request is valid"""
        if "group_id" not in data:
            return False

        group_id = data["group"]

        # Group must exist
        group_repo = GroupRepository()
        group = group_repo.fetch(group_id)
        if not group:
            return False

        # User must be a member of this group
        if group_id not in user.groups:
            return False

        # User must not be the group maintainer
        if user.id != group.maintainer.id:
            return False

        return True

    def _perform_request(self, user, data):
        """Removes the user from the group"""
        groups = user.groups
        groups.remove(data["group_id"])
        self._persist_user(user)

# - Delete (private) group
#   - Data: Group ID, User ID (from get_curr_user)
#   - Server-Side Checks:
#       - The Group ID is private.
#       - Current User ID is a member of Group ID
#       - Current User ID is the maintainer of Group ID
#       - @TODO(halstea2) Can a group be deleted if there are still non-maintainer
#         members associated with it?
#   - Side Effects:
#       - Delete all associated deadlines
class DeleteGroupHandler(AsyncRequestHandler):
    @tornado.web.authenticated
    def async_post(self):
        pass

# - Add member to group
#   - Data: Group ID, New User ID
#   - Server-Side Checks:
#       - New User ID must be in same parent group as current user ID
#       - Current user must be member of group ID
class AddMemberHandler(AsyncRequestHandler):
    @tornado.gen.coroutine
    @tornado.web.authenticated
    def async_post(self):
        pass

# - Get members of parent group (for 'Add member' auto-complete)
#   - Data: Parent Group ID
class GetMembersOfParentHandler(AsyncRequestHandler):
    # @TODO(halstea2) - Extract user auth and data checking to base class
    @tornado.gen.coroutine
    @tornado.web.authenticated
    def get(self):
        pass

# - Create subgroup (only if parent is public)
#   - Data: Course ID, Section ID, name, desc, type (inferred), user id (from get_curr_user)
#   - Server-Side Checks:
#       - Current user is a member of the parent group of the new subgroup ID
#   @TODO(halstea2) - Save for last
#   
class CreateSubgroupHandler(AsyncRequestHandler):
    @tornado.gen.coroutine
    @tornado.web.authenticated
    def async_post(self):
        pass

# - Get course list (for 'Create subgroup' auto-complete)
#   - Data: All courses?
class GetCourseListHandler(AsyncRequestHandler):
    # @TODO(halstea2) - Extract user auth and data checking to base class
    @tornado.gen.coroutine
    @tornado.web.authenticated
    def get(self):
        pass

# - Add deadline
#   - Data: Name (autocomplete), Datetime, group ID, notes
#   - Server-Side Checks:
#       - Current user is a member of this group ID
class AddDeadlineHandler(AsyncRequestHandler):
    @tornado.gen.coroutine
    @tornado.web.authenticated
    def async_post(self):
        pass

# - Get existing deadline names for the group (for 'Add deadline' auto-complete)
#   - Data: Group ID
class GetGroupDeadlinesHandler(AsyncRequestHandler):
    @tornado.gen.coroutine
    @tornado.web.authenticated
    def get(self):
        pass

# ../profile
# Required Handlers
# - Edit Name
#   - Data: Name
#   - Server-side Checks: None

# - 
#   - Data: Group ID
class UpdateNameHandler(AsyncRequestHandler):
    """Async Handler for updating a user's name"""

    def _valid_request(self, user, data):
        """Verify that the 'update name' request is valid"""
        print "update name handler"
        return "name" in data

    def _perform_request(self, user, data):
        """Update the user's name"""
        user.name = data["name"]
        print user.name
        self._persist_user(user)


# - Edit Email
#   - Data: Email
#   - Server-side Checks:
#       - Require email activation
class UpdateEmailHandler(AsyncRequestHandler):
    """Async Handler for updating a user's email"""

    def _valid_request(self, user, data):
        """Verify that the 'update email' request is valid"""

        return "email" in data

    def _perform_request(self, user, data):
        """Update the user's name"""
        unique = str(uuid.uuid4())

        user.email = data["email"]
        user.confirmed = False
        user.confirmUUID = unique
        self._persist_user(user)

        ## Send a verification email to the user
        m = CukeMail()
        m.send_verification(unique, user.email)

#@TODO(halstea2) - implement this?
# - Gravatar?
