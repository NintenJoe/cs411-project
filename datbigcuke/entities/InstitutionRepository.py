"""Module for Institution repository."""

__author__ = 'Eunsoo Roh'
__copyright__ = 'Copyright 2014 Bigdatcuke Project'
__email__ = 'roh7@illinois.edu'


from datbigcuke.entities.Institution import Institution
from datbigcuke.entities.AbstractRepository import AbstractRepository
import datbigcuke.db
import operator


class InstitutionRepository(AbstractRepository):

    def __init__(self):
        super(InstitutionRepository, self).__init__(Institution)

    def persist(self, inst):
        super(InstitutionRepository, self).persist(inst)

        delta = inst.get_delta()
        delta.pop('id', None)  # make sure id does not exist
        newgroup = delta.pop('group_id', None)  # make sure group does not exist
        if inst.id is None:
            # persisting new institution object is not supported
            raise NotImplementedError()
        elif newgroup is not None:
            # update group reference
            with self._conn.cursor() as cursor:
                cursor.execute('UPDATE `academic_entity` '
                               'SET `group_id`=? WHERE `id`=?',
                               (newgroup, inst.id))

        return inst

    def fetch(self, inst_id):
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `id`, `name`, `group_id` '
                           'FROM `institution` NATURAL JOIN `academic_entity`'
                           'WHERE `id`=?', (inst_id,))
            return self._fetch_inst(cursor)

    def fetch_all(self):
        inst_list = []
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `id`, `name`, `group_id` '
                           'FROM `institution` NATURAL JOIN `academic_entity`')
            for result in self._fetch_all_dict(cursor):
                inst_list.append(self._create_entity(data=result))

        return inst_list
        
    def _fetch_inst(self, cursor):
        result = self._fetch_dict(cursor)
        if result is not None:
            return self._create_entity(data=result)
