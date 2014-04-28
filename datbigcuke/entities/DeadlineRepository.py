"""Module for User repository.

DeadlineRepository offers access and persistence of Deadline objects.
"""

__author__ = 'Kyle Nusbaum'
__copyright__ = 'Copyright 2014 Bigdatcuke Project'
__email__ = 'kjnusba2@illinois.edu'


from datbigcuke.entities.Deadline import Deadline
from datbigcuke.entities.AbstractRepository import AbstractRepository
import datbigcuke.db
import operator


class DeadlineRepository(AbstractRepository):

    def __init__(self):
        super(DeadlineRepository, self).__init__(Deadline)

    def persist(self, deadline):
        super(DeadlineRepository, self).persist(deadline)

        delta = deadline.get_delta()
        delta.pop('id', None) # make sure id does not exist
        
        if deadline.id is None:
    
            with self._conn.cursor() as cursor:
                cursor.execute('INSERT INTO `deadline` (origin, deadline) ' 
                               'VALUES (?,?);',
                               (delta['origin'], delta['deadline']))


        else:
            if delta:
                assert 'id' not in delta
                keys = delta.keys()
                args = list(delta.values())
                args.append(user.id)
                query = ','.join('`{}`=?'.format(k) for k in keys)
                with self._conn.cursor() as cursor:
                    cursor.execute('UPDATE `deadline` '
                                   'SET {} WHERE `id`=?'.format(query),
                                   args)
                
            
    def fetch(self, deadline_id):
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `id`, `origin`, `deadline` '
                           'FROM `deadline` '
                           'WHERE `id`=?', (deadline_id,))
        return self._fetch_deadline(cursor)

    def fetch_all(self):
        deadline_list = []
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `id`, `origin`, `deadline` '
                           'FROM `deadline` ')
        for result in self._fetch_all_dict(cursor):
            deadline_list.append(self._create_entity(data=result))
            
        return deadline_list

    def _fetch_deadline(self, cursor):
        result = self._fetch_dict(cursor)
        if result is not None:
            return self._create_entity(data=result)
