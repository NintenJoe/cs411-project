"""Module for Class entity."""

__author__ = 'Eunsoo Roh'
__copyright__ = 'Copyright 2014 Bigdatcuke Project'
__email__ = 'roh7@illinois.edu'


from datbigcuke.entities.AbstractEntity import AbstractEntity


class Class(AbstractEntity):
    _ATTRIB_TO_DATA = {
        '_id' : 'id',
        '_institution': 'institution_id',
        '_term': 'term_id',
        '_name': 'class_name',
        '_title': 'title',
        '_course_name': 'name',
        '_group': 'group_id',
    }

    def __init__(self, data=None):
        super(Class, self).__init__(data=data)

    @property
    def id(self):
        return self._id

    @property
    def institution(self):
        return self._institution

    @property
    def term(self):
        return self._term

    @property
    def name(self):
        return self._name

    @property
    def title(self):
        return self._title

    @property
    def course_name(self):
        return self._course_name

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        self._group = value

    def validate(self):
        return True
