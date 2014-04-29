"""Module for Deadline entity."""

__author__ = 'Kyle Nusbaum'
__copyright__ = 'Copyright 2014 Bigdatcuke Project'
__email__ = 'kjnusba2@illinois.edu'


from datbigcuke.entities.AbstractEntity import AbstractEntity
import os
import hashlib
import urllib


class Deadline(AbstractEntity):
    _meta = None
    _ATTRIB_TO_DATA = {
        '_id' : 'id',
        '_name' : 'name',
        '_group_id' : 'group_id',
        '_deadline' : 'deadline',
        '_type' : 'type',
        '_meta' : 'meta',
        '_group' : 'group'
    }

    def __init__(self, data=None):
        super(Deadline, self).__init__(data=data)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def group_id(self):
        return self._group_id

    @group_id.setter
    def group_id(self, value):
        self._group_id = value

    @property
    def deadline(self):
        return self._deadline

    @deadline.setter
    def deadline(self, value):
        self._deadline = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def meta(self):
        return self._meta

    @meta.setter
    def meta(self, value):
        self._meta = value

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        self._group = value

    def validate(self):
        return True
