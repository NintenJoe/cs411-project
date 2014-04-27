"""Module for User entity."""

__author__ = 'Eunsoo Roh'
__copyright__ = 'Copyright 2014 Bigdatcuke Project'
__email__ = 'roh7@illinois.edu'


from datbigcuke.entities.AbstractEntity import AbstractEntity
import os
import hashlib


class User(AbstractEntity):
    # @TODO(halstea2) Add maintainer mapping to this dictionary.
    _ATTRIB_TO_DATA = {
        '_id' : 'id',
        '_email' : 'email',
        '_name' : 'name',
        '_hashedPassword' : 'password',
        '_salt' : 'salt',
        '_confirmed' : 'confirmed',
        '_confirmUUID' : 'confirmUUID',
        '_groups' : 'groups',
    }

    def __init__(self, data=None):
        super(User, self).__init__(data=data)
        self._plainPassword = None

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def hashedPassword(self):
        return self._hashedPassword

    @property
    def password(self):
        return self._plainPassword

    @property
    def confirmed(self):
        return self._confirmed

    @property
    def confirmUUID(self):
        return self._confirmUUID

    @confirmUUID.setter
    def confirmUUID(self, value):
        self._confirmUUID = value
    
    @password.setter
    def password(self, value):
        # passwords are hashed with random 40-digit hexadecimal salt 
        salt = os.urandom(20).encode('hex')
        self._plainPassword = value
        self._salt = salt
        self._hashedPassword = hashlib.sha1(salt + value).hexdigest()

    def match_password(self, password):
        hashedPassword = hashlib.sha1(self._salt + password).hexdigest()
        return self._hashedPassword == hashedPassword

    @property
    def groups(self):
        return self._groups

    @groups.setter
    def groups(self, value):
        self._groups = list(value)

    def validate(self):
        # TODO(roh7): implement proper validation
        return True
