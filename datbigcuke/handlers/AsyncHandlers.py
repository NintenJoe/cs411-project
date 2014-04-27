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
#Required Handlers


# Example raw json call
#    <button onclick="(
#        function (e, obj) {
#            var data1 = {};
#            data1['group'] = 1234;
#            $.ajax({
#                type: 'POST',
#                url: '/leave-group',
#                data: {'data': JSON.stringify(data1)},
#                dataType: 'json',
#                success: function(data) {
#                    console.log(data);
#                },
#                error: function(data) {
#                    console.log(data);
#                }
#            });
#        })(event, this)"> Test Leave Group </button>

class LeaveGroupHandler(AsyncRequestHandler):
    """Async Handler for leaving a group"""

    @tornado.web.authenticated
    def post(self):

        user = self.get_current_user()
        data = self.get_argument("data", default=None)
        data = json.loads(data)

        # 'Logged-in' user must be defined
        if not user:
            return

        # Value list must be defined
        if not data:
            return

        if not self._valid_request(user, "", data):
            return

        self._perform_request(user, "", data)
       
    # The name parameter is ignored. Needs to be factored but no time.
    def _valid_request(self, user, name, data):
        """Verify that the 'leave group' request is valid"""

        if "group" not in data:
            return False

        group_id = data[u"group"]

        # Group must exist
        group_repo = GroupRepository()
        group = group_repo.fetch(group_id)
        if not group:
            print "group doesn't exist"
            return False

        # User must be a member of this group
        if group_id not in user.groups:
            return False

        # User must not be the group maintainer
        if user.id != group.maintainer.id:
            return False

        return True

    # The name parameter is ignored. Needs to be factored but no time.
    def _perform_request(self, user, name, data):
        """Removes the user from the group"""
        groups = user.groups
        groups.remove(data[u"group"])
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
    """Async Handler for leaving a group"""

    @tornado.web.authenticated
    def post(self):

        user = self.get_current_user()
        data = self.get_argument("data", default=None)
        # Keys are unicode after json.loads conversion
        data = json.loads(data)


        # 'Logged-in' user must be defined
        if not user:
            return

        # Value list must be defined
        if not data:
            return

        if not self._valid_request(user, "", data):
            return

        self._perform_request(user, "", data)
       
    # The name parameter is ignored. Needs to be factored but no time.
    def _valid_request(self, user, name, data):
        """Verify that the 'leave group' request is valid"""

        if "group" not in data:
            return False

        # Keys are unicode after json.loads conversion
        group_id = data[u"group"]

        # Group must exist
        group_repo = GroupRepository()
        group = group_repo.fetch(group_id)
        if not group:
            print "group doesn't exist"
            return False

        # Group must be private
        # @TODO(halstea2) How is 'private' represented in database? Assume
        # that Group.type = 'private' is how it's represened. Change otherwise
        print "Make sure we clarify how 'private' groups are represented in the database"
        if group.type != "private":
            return False

        # User must be a member of this group
        if group_id not in user.groups:
            return False

        # User must be the group maintainer
        if user.id == group.maintainer.id:
            return False

        return True

    # The name parameter is ignored. Needs to be factored but no time.
    def _perform_request(self, user, name, data):
        """Removes the user from the group"""

        # @TODO(halstea2) Not sure canonical way to delete group. Think Eunsoo
        # wanted to enforce that no members were present in the group before
        # deleting.

        print "No remove function is implemented in the GroupRepository"
        #groups = user.groups
        #groups.remove(data[u"group"])
        #self._persist_user(user)


# - Add member to group
#   - Data: Group ID, New User ID
#   - Server-Side Checks:
#       - New User ID must be in same parent group as current user ID
#       - Current user must be member of group ID
class AddMemberHandler(AsyncRequestHandler):
    @tornado.web.authenticated
    # @TODO(halstea2) We chould create a 'complex' async handler base that
    # is aware of a dictionary of values
    def post(self):
        curr_user = self.getCurrent_user()
        values =  self.get_argument("values", default=None)

        if not user:
            return

        if not data:
            return

        # We don't need the 'name' field. It's encoded in the data dictionary
        # Keys are unicode after json.loads conversion
        data = json.loads(data)
        if not self._valid_request(user, "", data):
            return

        self._perform_request(user, "", data)
        pass

    def _valid_request(self, user, name, values):
        # Malformed request
        if u"group_id" not in values or u"user_id" not in values:
            return False

        # Malformed request
        group_id = values[u"group_id"]
        user_id = values["uuser_id"]
        if not group_id or not user_id:
            return False

        #@TODO(halstea2) We need a mechanism in Group to retrieve the parent
        # and then verify the curr_user and new_user are members of it.

        # Current user must be a member of the subgroup they're trying to add a
        # member to
        if group_id not in user.groups:
            return False

        # New user is already a member of the group
        new_user_repo = UserRepository()
        new_user = new_user_repo.fetch(user_id)
        new_user_repo.close()
        if group_id in new_user.groups:
            return False

        return True

    def _perform_request(self, user, name, values):
        group_id = values[u"group_id"]
        user_id = values[u"user_id"]

        new_user_repo = UserRepository()
        new_user = new_user_repo.fetch(user_id)
        new_user_repo.close()

        new_user.append(group_id)
        self._persist_user(new_user)
        pass

# - Get members of parent group (for 'Add member' auto-complete)
#   - Data: Parent Group ID
class GetMembersOfParentHandler(AsyncRequestHandler):
    # @TODO(halstea2) - Extract user auth and data checking to base class
    def get(self):
        pass

# - Create subgroup (only if parent is public)
#   - Data: Course ID, Section ID, name, desc, type (inferred), user id (from get_curr_user)
#   - Server-Side Checks:
#       - Current user is a member of the parent group of the new subgroup ID
#   @TODO(halstea2) - Save for last
#   
class CreateSubgroupHandler(AsyncRequestHandler):
    def _valid_request(self, user, name, values):
        pass

    def _perform_request(self, user, name, values):
        pass

# - Get course list (for 'Create subgroup' auto-complete)
#   - Data: All courses?
class GetCourseListHandler(AsyncRequestHandler):
    # @TODO(halstea2) - Extract user auth and data checking to base class
    @tornado.web.authenticated
    def get(self):
        pass

# - Add deadline
#   - Data: Name (autocomplete), Datetime, group ID, notes
#   - Server-Side Checks:
#       - Current user is a member of this group ID
class AddDeadlineHandler(AsyncRequestHandler):
    def _valid_request(self, user, name, values):
        pass

    def _perform_request(self, user, name, values):
        pass

# - Get existing deadline names for the group (for 'Add deadline' auto-complete)
#   - Data: Group ID
class GetGroupDeadlinesHandler(AsyncRequestHandler):
    @tornado.web.authenticated
    def get(self):
        pass

## - Schedule endpoint
class ScheduleHandler(AsyncRequestHandler):
    def _valid_request(self, user, name, values):
        pass

    def _perform_request(self, user, name, values):
        pass
    pass


# /profile Request Handlers

# - Edit Name
#   - Data: Name
#   - Server-side Checks: None
class UpdateNameHandler(AsyncRequestHandler):
    """Async Handler for updating a user's name"""

    # Assumptions: User is authenticated. attr is string (decoded to utf-8).
    def _valid_request(self, user, attr, value):
        """Verify that the 'update name' request is valid"""
        if not hasattr(user, attr):
            return False

        if len(value) != 1:
            return False

        return True

    # Assumption: User is authenticated. attr exists. Value is list of length 1
    def _perform_request(self, user, attr, value):
        """Perform the update request. For simple (read: single attribute
        updates the 'name' is the attribute and the 'value' is a list of len 1
        containing the value. This isn't the case for multi-attribute edits."""

        value = value[0].decode("utf-8")
        setattr(user, attr, value)
        self._persist_user(user)


# - Edit Email
#   - Data: Email
#   - Server-side Checks:
#       - Require email activation
#       - Clear cookies
class UpdateEmailHandler(AsyncRequestHandler):
    """Async Handler for updating a user's email"""

    # Assumptions: User is authenticated. attr is string (decoded to utf-8).
    def _valid_request(self, user, attr, value):
        """Verify that the 'update email' request is valid"""
        if not hasattr(user, attr):
            return False

        if len(value) != 1:
            return False

        return True

    # Assumption: User is authenticated. attr exists. Value is list of length 1
    def _perform_request(self, user, attr, value):
        """Perform the update request. For simple (read: single attribute
        updates the 'name' is the attribute and the 'value' is a list of len 1
        containing the value. This isn't the case for multi-attribute edits."""

        value = value[0].decode("utf-8")
        setattr(user, attr, value)

        unique = str(uuid.uuid4())
        user.confirmed = False
        user.confirmUUID = unique

        self._persist_user(user)

        ## Send a verification email to the user
        m = CukeMail()
        m.send_verification(unique, user.email)
        self.clear_cookie(self.cookie_name)
