"""Module for Term entity."""

__author__ = 'Eunsoo Roh'
__copyright__ = 'Copyright 2014 Bigdatcuke Project'
__email__ = 'roh7@illinois.edu'


from datbigcuke.entities.AbstractEntity import AbstractEntity


class Term(AbstractEntity):
    _ATTRIB_TO_DATA = {
        '_id' : 'id',
        '_institution': 'institution_id',
        '_year': 'year',
        '_seq_index': 'sindex',
        '_name': 'name',
    }

    def __init__(self, data=None):
        super(Term, self).__init__(data=data)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def year(self):
        return self._year

    @property
    def institution(self):
        return self._institution

    @property
    def seq_index(self):
        return self._gseq_index

    def validate(self):
        return True
