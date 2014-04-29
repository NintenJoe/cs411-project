"""Module for User repository.

DeadlineRepository offers access and persistence of Deadline objects.
"""

__author__ = 'Kyle Nusbaum'
__copyright__ = 'Copyright 2014 Bigdatcuke Project'
__email__ = 'kjnusba2@illinois.edu'

from datbigcuke.entities.DeadlineMetadata import DeadlineMetadata
from datbigcuke.entities.DeadlineMetadataRepository import DeadlineMetadataRepository
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
                cursor.execute('INSERT INTO `deadline` (name, group_id, deadline, type) ' 
                               'VALUES (?,?);',
                               (delta['name'], delta['group_id'], delta['deadline'], delta['type']))

                cursor.execute('SELECT `id`, `name`, `group_id`, `deadline`, `type` '
                               'FROM `deadline` '
                               'WHERE `id`=LAST_INSERT_ID()')
                deadline = self._fetch_group(cursor)

                if deadline.meta:
                    deadline.meta.deadline_id = deadline.id
                    dmr = DeadlineMetadataRepository()
                    dmr.persist(deadline.meta)
                    
        else:
            if deadline.meta:
                dmr = DeadlineMetadataRepository()
                dmr.persist(deadline.meta)
                
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

        return deadline
                
            
    def fetch(self, deadline_id):
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `d`.`id`, `d`.`name`, `d`.`group_id`, `d`.`deadline`, `d`.`type`, `g`.`name` as `group` '
                           'FROM `deadline` as `d` '
                           'JOIN `group` as `g` '
                           'ON `g`.`id` = `d`.`group_id` '
                           'WHERE `d`.`id`=?', (deadline_id,))
            return self._fetch_deadline(cursor)

    def fetch_all(self):
        deadline_list = []
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `d`.`id`, `d`.`name`, `d`.`group_id`, `d`.`deadline`, `d`.`type`, `g`.`name` as `group` '
                           'FROM `deadline` as `d`'
                           'JOIN `g` as `g` '
                           'ON `g`.`id` = `d`.`group_id` ')
            for result in self._fetch_all_dict(cursor):
                deadline_list.append(self._create_entity(data=result))
            
        return deadline_list

    def deadlines_for_user(self, user_id):
        deadline_list = []
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT DISTINCT `d`.`id`, `d`.`name`, `d`.`group_id`, `d`.`deadline`, `d`.`type`, `dm`.`user_id`, `dm`.`deadline_id`, `dm`.`notes`, `g`.`name` as `group` '
                           'FROM `deadline` as `d` '
                           'LEFT JOIN `deadline_metadata` as `dm` '
                           'ON `dm`.`deadline_id` = `d`.`id`'
                           'JOIN `group` as `g` '
                           'ON `g`.`id` = `d`.`group_id` '
                           'JOIN `group_membership` as `gm` '
                           'ON `gm`.`group_id` = `g`.`id` '
                           'WHERE `dm`.`user_id` =? '
                           'OR (`gm`.`member_id` =? '
                           '    AND (`d`.`type` = \'END\' ' 
                           '         OR `d`.`type` = \'COM\')) '
                           'ORDER BY `d`.`deadline` ', (user_id, user_id))

            for result in self._fetch_all_dict(cursor):
                deadline = self._create_entity(data=result)
                deadlineMeta = None
                if result['deadline_id']:
                    deadlineMeta = DeadlineMetadata()
                    deadlineMeta.user_id = result['user_id']
                    deadlineMeta.deadline_id = result['id']
                    deadlineMeta.notes = result['notes']
                deadline.meta = deadlineMeta
                deadline_list.append(deadline)

        return deadline_list


    def deadlines_for_user_for_group(self, user_id, group_id):
        deadline_list = []
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT DISTINCT `d`.`id`, `d`.`name`, `d`.`group_id`, `d`.`deadline`, `d`.`type`, `dm`.`user_id`, `dm`.`deadline_id`, `dm`.`notes`, `g`.`name` as `group` '
                           'FROM `deadline` as `d` '
                           'LEFT JOIN `deadline_metadata` as `dm` '
                           'ON `dm`.`deadline_id` = `d`.`id`'
                           'JOIN `group` as `g` '
                           'ON `g`.`id` = `d`.`group_id` '
                           'JOIN `group_membership` as `gm` '
                           'ON `gm`.`group_id` = `g`.`id` '
                           'WHERE (`dm`.`user_id` =? '
                           'OR (`gm`.`member_id` =? '
                           '    AND (`d`.`type` = \'END\' ' 
                           '         OR `d`.`type` = \'COM\'))) '
                           'AND `d`.`group_id` =? '
                           'ORDER BY `d`.`deadline` ', (user_id, user_id, group_id))

            for result in self._fetch_all_dict(cursor):
                deadline = self._create_entity(data=result)
                deadlineMeta = None
                if result['deadline_id']:
                    deadlineMeta = DeadlineMetadata()
                    deadlineMeta.user_id = result['user_id']
                    deadlineMeta.deadline_id = result['id']
                    deadlineMeta.notes = result['notes']
                deadline.meta = deadlineMeta
                deadline_list.append(deadline)

        return deadline_list


    def deadlines_for_group(self, group_id):
        deadline_list = []
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `d`.`id`, `d`.`name`, `d`.`group_id`, `d`.`deadline`, `d`.`type`, `g`.`name` as `group` '
                           'FROM `deadline` AS `d` '
                           'JOIN `group` as `g` '
                           'ON `g`.`id` = `d`.`group_id` '
                           'WHERE `d`.`group_id` =?', (group_id,))
            
            for result in self._fetch_all_dict(cursor):
                deadline_list.append(self._create_entity(data=result))
        
    def deadline_for_user(self, user_id, deadline_id):
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `d`.`id`, `d`.`name`, `d`.`group_id`, `d`.`deadline`, `d`.`type`, `dm`.`user_id`, `dm`.`deadline_id`, `dm`.`notes`, `g`.`name` as `group` '
                           'FROM `deadline` AS `d` '
                           'JOIN `deadline_metadata` as `dm` '
                           'ON `dm`.`deadline_id` = `d`.`id` '
                           'JOIN `group` as `g` '
                           'ON `g`.`id` = `d`.`group_id` '
                           'WHERE `d`.`id` =?', (deadline_id,))
            
            result = self._fetch_dict(cursor)
            deadline = self._create_entity(data=result)
            deadlineMeta = None
            if result['deadline_id']:
                deadlineMeta = DeadlineMetadata()
                deadlineMeta.user_id = result['user_id']
                deadlineMeta.deadline_id = result['id']
                deadlineMeta.notes = result['notes']
            deadline.meta = deadlineMeta
            return deadline



    def _fetch_deadline(self, cursor):
        result = self._fetch_dict(cursor)
        if result is not None:
            return self._create_entity(data=result)
