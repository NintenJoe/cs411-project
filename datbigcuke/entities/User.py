"""Module for User entity."""

__author__ = 'Eunsoo Roh'
__copyright__ = 'Copyright 2014 Bigdatcuke Project'
__email__ = 'roh7@illinois.edu'


from datbigcuke.entities.AbstractEntity import AbstractEntity
import os
import hashlib
import urllib


class User(AbstractEntity):
    _ATTRIB_TO_DATA = {
        '_id' : 'id',
        '_email' : 'email',
        '_name' : 'name',
        '_hashedPassword' : 'password',
        '_salt' : 'salt',
        '_confirmed' : 'confirmed',
        '_confirmUUID' : 'confirmUUID',
        '_refreshTok' : 'refreshTok',
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
    def iconBigURL(self):
        # NOTE(ciurej2): Added this function to simply gravatar icon calculation.
        # Can be moved or changed as needed.
        # SEE: https://en.gravatar.com/site/implement/hash/
        url = 'http://www.gravatar.com/avatar/'
        url += hashlib.md5(self.email.strip().lower().encode()).hexdigest() + '?'
        url += urllib.urlencode({ 's': "180" })

        return url

    @property
    def iconSmallURL(self):
        # TODO(ciurej2): Refactor this functionality to eliminate duplication.
        url = 'http://www.gravatar.com/avatar/'
        url += hashlib.md5(self.email.strip().lower().encode()).hexdigest() + '?'
        url += urllib.urlencode({ 's': "20" })

        return url

    @property
    def hashedPassword(self):
        return self._hashedPassword

    @property
    def password(self):
        return self._plainPassword

    @property
    def confirmed(self):
        return self._confirmed

    @confirmed.setter
    def confirmed(self, value):
        self._confirmed = value

    @property
    def confirmUUID(self):
        return self._confirmUUID

    @confirmUUID.setter
    def confirmUUID(self, value):
        self._confirmUUID = value

    @property
    def refreshTok(self):
        return self._refreshTok

    @refreshTok.setter
    def refreshTok(self, value):
        self._refreshTok = value

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

