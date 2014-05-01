"""Module for Class repository."""

__author__ = 'Eunsoo Roh'
__copyright__ = 'Copyright 2014 Bigdatcuke Project'
__email__ = 'roh7@illinois.edu'


from datbigcuke.entities.Class import Class
from datbigcuke.entities.AbstractRepository import AbstractRepository
import datbigcuke.db
import operator


class ClassRepository(AbstractRepository):

    def __init__(self):
        super(ClassRepository, self).__init__(Class)

    def persist(self, inst):
        super(ClassRepository, self).persist(inst)

        delta = inst.get_delta()
        delta.pop('id', None)  # make sure id does not exist
        newgroup = delta.pop('group_id', None)  # make sure group does not exist
        if inst.id is None:
            # persisting new class object is not supported
            raise NotImplementedError()
        elif newgroup is not None:
            # update group reference
            with self._conn.cursor() as cursor:
                cursor.execute('UPDATE `academic_entity` '
                               'SET `group_id`=? WHERE `id`=?',
                               (newgroup, inst.id))

        return inst

    def fetch(self, class_id):
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `id`, `institution_id`, `term_id`, `name`,'
                           '`title`, `class_name`, `group_id` '
                           'FROM `class` NATURAL JOIN `academic_entity`'
                           'WHERE `id`=?', (class_id,))
            return self._fetch_class(cursor)

    def fetch_all(self):
        class_list = []
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `id`, `institution_id`, `term_id`, `name`,'
                           '`title`, `class_name`, `group_id` '
                           'FROM `class` NATURAL JOIN `academic_entity`')
            for result in self._fetch_all_dict(cursor):
                class_list.append(self._create_entity(data=result))

        return class_list

    def _fetch_class(self, cursor):
        result = self._fetch_dict(cursor)
        if result is not None:
            return self._create_entity(data=result)

    def find_classes_with_name_prefix(self, term, prefix):
        class_list = []
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `id`, `institution_id`, `term_id`, `name`,'
                           '`title`, `class_name`, `group_id` '
                           'FROM `class` NATURAL JOIN `academic_entity`'
                           'WHERE `term_id`=? AND `class_name` LIKE ?',
                           (term.id, '{!s}%'.format(prefix)))
            for result in self._fetch_all_dict(cursor):
                class_list.append(self._create_entity(data=result))

        return class_list
