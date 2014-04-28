"""Module for Deadline entity."""

__author__ = 'Kyle Nusbaum'
__copyright__ = 'Copyright 2014 Bigdatcuke Project'
__email__ = 'kjnusba2@illinois.edu'


from datbigcuke.entities.AbstractEntity import AbstractEntity
import os
import hashlib
import urllib


class Deadline(AbstractEntity):
    _ATTRIB_TO_DATA = {
        '_id' : 'id',
        '_origin' : 'origin',
        '_deadline' : 'deadline',
    }

    def __init__(self, data=None):
        super(Deadline, self).__init__(data=data)

    @property
    def id(self):
        return self._id

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = value

    @property
    def deadline(self):
        return self._deadline

    @deadline.setter
    def deadline(self, value):
        self._deadline = value

    def validate(self):
        return True
