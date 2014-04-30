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

    def persist(self, term):
        super(TermRepository, self).persist(term)

        delta = term.get_delta()
        delta.pop('id', None)  # make sure id does not exist
        newgroup = delta.pop('group_id', None)  # make sure group does not exist
        if term.id is None:
            # persisting new term object is not supported
            raise NotImplementedError()
        elif newgroup is not None:
            # update group reference
            with self._conn.cursor() as cursor:
                cursor.execute('UPDATE `academic_entity` '
                               'SET `group_id`=? WHERE `id`=?',
                               (newgroup, term.id))

        return term

    def fetch(self, term_id):
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `id`, `institution_id`, `year`, '
                           '`sindex`, `name`, `group_id` '
                           'FROM `term` NATURAL JOIN `academic_entity`'
                           'WHERE `id`=?', (term_id,))
            return self._fetch_term(cursor)

    def fetch_all(self):
        term_list = []
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `id`, `institution_id`, `year` '
                           '`sindex`, `name`, `group_id` '
                           'FROM `term` NATURAL JOIN `academic_entity`')
            for result in self._fetch_all_dict(cursor):
                term_list.append(self._create_entity(data=result))

        return term_list

    def fetch_terms_by_year(self, inst, year):
        term_list = []
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `id`, `institution_id`, `year` '
                           '`sindex`, `name`, `group_id` '
                           'FROM `term` NATURAL JOIN `academic_entity`'
                           'WHERE `institution_id`=? AND `year`=?',
                           (inst.id, year))
            for result in self._fetch_all_dict(cursor):
                term_list.append(self._create_entity(data=result))
        return term_list

    def fetch_term_by_year_index(self, inst, year, sindex):
        term_list = []
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `id`, `institution_id`, `year` '
                           '`sindex`, `name`, `group_id` '
                           'FROM `term` NATURAL JOIN `academic_entity`'
                           'WHERE `institution_id`=? AND `year`=? '
                           'AND `sindex`=?',
                           (inst.id, year, sindex))
            for result in self._fetch_all_dict(cursor):
                term_list.append(self._create_entity(data=result))
        if not term_list:
            return None
        return term_list[0]
        
    def _fetch_term(self, cursor):
        result = self._fetch_dict(cursor)
        if result is not None:
            return self._create_entity(data=result)
