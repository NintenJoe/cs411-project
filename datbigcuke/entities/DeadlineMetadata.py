"""Module for DeadlineMetadata entity."""

__author__ = 'Kyle Nusbaum'
__copyright__ = 'Copyright 2014 Bigdatcuke Project'
__email__ = 'kjnusba2@illinois.edu'


from datbigcuke.entities.AbstractEntity import AbstractEntity
import os
import hashlib
import urllib


class DeadlineMetadata(AbstractEntity):
    _ATTRIB_TO_DATA = {
        '_user_id' : 'user_id',
        '_deadline_id' : 'deadline_id';
        '_name' : 'name',
        '_notes' : 'notes',
    }

    def __init__(self, data=None):
        super(DeadlineMetadata, self).__init__(data=data)

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def deadline_id(self):
        return self._deadline_id

    @deadline_id.setter
    def deadline_id(self, value):
        self._deadline_id = value
        
    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, value):
        self._notes = value

    def validate(self):
        return True
