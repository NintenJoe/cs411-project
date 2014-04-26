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

from datbigcuke.handlers.BaseHandlers import AsyncRequestHandler


# @TODO(halstea2) sanitize user data


class TestHandler(AsyncRequestHandler):
    def post(self):
        data = self.get_argument("data", None)
        if data:
            print str(datetime.datetime.now()) +\
                  " Received: " +\
                  str(json.dumps(data,
                                 sort_keys=True,
                                 indent=4,
                                 separators=(',', ': ')
                     )
            )
            self.write(json.dumps({"date": str(datetime.datetime.now()),
                                   "Status": 200}))
        else:
            print str(datetime.datetime.now()) + " Received: None"
            self.write(json.dumps({"date": str(datetime.datetime.now()),
                                   "Status": 404}))
