"""Module for Institution entity."""

__author__ = 'Eunsoo Roh'
__copyright__ = 'Copyright 2014 Bigdatcuke Project'
__email__ = 'roh7@illinois.edu'


from datbigcuke.entities.AbstractEntity import AbstractEntity


class Institution(AbstractEntity):
    _ATTRIB_TO_DATA = {
        '_id' : 'id',
        '_name': 'name',
        '_group': 'group_id',
    }

    def __init__(self, data=None):
        super(Institution, self).__init__(data=data)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        self._group = value

    def validate(self):
        return True
