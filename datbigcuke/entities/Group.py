"""Module for Group entity."""

__author__ = 'Eunsoo Roh'
__copyright__ = 'Copyright 2014 Bigdatcuke Project'
__email__ = 'roh7@illinois.edu'


from datbigcuke.entities.AbstractEntity import AbstractEntity
import os
import hashlib


class Group(AbstractEntity):
    _ATTRIB_TO_DATA = {
        '_id' : 'id',
        '_name' : 'name',
        '_description' : 'description',
        '_type' : 'type',
    }

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
    def maintainer(self):
        # @TODO(halstea2) Add maintainer to database and return
        # a User object (or None)
        return None

    @maintainer.setter
    def maintainer(self, value):
        # @TODO(halstea2) Add maintainer to database
        pass

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = type

    def validate(self):
        # TODO(roh7): implement proper validation
        return True
