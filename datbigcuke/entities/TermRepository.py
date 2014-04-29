"""Module for Term repository."""

__author__ = 'Eunsoo Roh'
__copyright__ = 'Copyright 2014 Bigdatcuke Project'
__email__ = 'roh7@illinois.edu'


from datbigcuke.entities.Term import Term
from datbigcuke.entities.AbstractRepository import AbstractRepository
import datbigcuke.db
import operator


class TermRepository(AbstractRepository):

    def __init__(self):
        super(TermRepository, self).__init__(Term)

    def fetch(self, term_id):
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `id`, `institution_id`, `year`, '
                           '`sindex`, `name` '
                           'FROM `term`'
                           'WHERE `id`=?', (term_id,))
            return self._fetch_term(cursor)

    def fetch_all(self):
        term_list = []
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `id`, `institution_id`, `year` '
                           '`sindex`, `name` '
                           'FROM `term`')
            for result in self._fetch_all_dict(cursor):
                term_list.append(self._create_entity(data=result))

        return term_list
        
    def _fetch_term(self, cursor):
        result = self._fetch_dict(cursor)
        if result is not None:
            return self._create_entity(data=result)
