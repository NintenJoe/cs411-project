"""Module for User repository.

DeadlineRepository offers access and persistence of Deadline objects.
"""

__author__ = 'Kyle Nusbaum'
__copyright__ = 'Copyright 2014 Bigdatcuke Project'
__email__ = 'kjnusba2@illinois.edu'

from datbigcuke.aggregation import *
from datbigcuke.entities.DeadlineMetadata import DeadlineMetadata
from datbigcuke.entities.DeadlineMetadataRepository import DeadlineMetadataRepository
from datbigcuke.entities.Deadline import Deadline
from datbigcuke.entities.AbstractRepository import AbstractRepository
from datbigcuke.entities.GroupRepository import GroupRepository
import datbigcuke.db
import operator
import math

class DeadlineRepository(AbstractRepository):

    def __init__(self):
        super(DeadlineRepository, self).__init__(Deadline)

    def persist(self, deadline):
        return self.raw_persist(deadline, True)

    def raw_persist(self, deadline, aggregate):
        super(DeadlineRepository, self).persist(deadline)

        delta = deadline.get_delta()
        delta.pop('id', None) # make sure id does not exist
        delta.pop('meta', None)

        if deadline.id is None:
            with self._conn.cursor() as cursor:
                cursor.execute('INSERT INTO `deadline` (name, group_id, deadline, type) ' 
                               'VALUES (?,?,?,?);',
                               (delta['name'], delta['group_id'], delta['deadline'], delta['type']))

                cursor.execute('SELECT `id`, `name`, `group_id`, `deadline`, `type` '
                               'FROM `deadline` '
                               'WHERE `id`=LAST_INSERT_ID()')
                new_deadline = self._fetch_deadline(cursor)
                
                if deadline.meta:
                    new_deadline.meta = deadline.meta
                    new_deadline.meta.deadline_id = new_deadline.id
                    new_deadline.meta.insert = True
                    dmr = DeadlineMetadataRepository()
                    dmr.persist(new_deadline.meta)
                    
                deadline = new_deadline
        else:
            if deadline.meta:
                dmr = DeadlineMetadataRepository()
                dmr.persist(deadline.meta)
                
            if delta:
                assert 'id' not in delta
                keys = delta.keys()
                args = list(delta.values())
                args.append(deadline.id)
                query = ','.join('`{}`=?'.format(k) for k in keys)
                with self._conn.cursor() as cursor:
                    cursor.execute('UPDATE `deadline` '
                                   'SET {} WHERE `id`=?'.format(query),
                                   args)
                    
        if aggregate:
            return self.perform_aggregation(deadline)
                
    def drop_metadata(self, deadline):
        with self._conn.cursor() as cursor:
            cursor.execute('DELETE FROM `deadline_metadata` '
                           'WHERE `deadline_id` =? AND `user_id` =?', (deadline.meta.deadline_id,deadline.meta.user_id))

    def delete(self, deadline_id):
        with self._conn.cursor() as cursor:
            cursor.execute('DELETE FROM `deadline` '
                           'WHERE `id` =? ', (deadline_id,))

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
                           'GROUP BY `d`.`id` '
                           'ORDER BY `d`.`deadline` ', (user_id, user_id))

            for result in self._fetch_all_dict(cursor):
                deadline = self._create_entity(data=result)
                deadlineMeta = None
                if result['user_id'] == user_id:
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
            cursor.execute('SELECT `d`.`id`, `d`.`name`, `d`.`group_id`, `d`.`deadline`, `d`.`type`, `dm`.`user_id`, `dm`.`deadline_id`, `dm`.`notes`, `g`.`name` as `group` '
                           'FROM `deadline` as `d` '
                           'LEFT JOIN `deadline_metadata` as `dm` '
                           'ON `dm`.`deadline_id` = `d`.`id`'
                           'JOIN `group` as `g` '
                           'ON `g`.`id` = `d`.`group_id` '
                           'JOIN `group_membership` as `gm` '
                           'ON `gm`.`group_id` = `g`.`id` '
                           'WHERE (`dm`.`user_id` =? '
                           '        OR (`gm`.`member_id` =? '
                           '             AND (`d`.`type` = \'END\' ' 
                           '                   OR `d`.`type` = \'COM\'))) '
                           'AND `d`.`group_id` =? '
                           'GROUP BY `d`.`id` '
                           'ORDER BY `d`.`deadline` ', (user_id, user_id, group_id))

            for result in self._fetch_all_dict(cursor):
                deadline = self._create_entity(data=result)
                deadlineMeta = None
                if result['user_id'] == user_id:
                    deadlineMeta = DeadlineMetadata()
                    deadlineMeta.user_id = result['user_id']
                    deadlineMeta.deadline_id = result['id']
                    deadlineMeta.notes = result['notes']
                deadline.meta = deadlineMeta
                deadline_list.append(deadline)
                print "Result: ", result
        print "List: ", deadline_list
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
                           'LEFT JOIN `deadline_metadata` as `dm` '
                           'ON `dm`.`deadline_id` = `d`.`id` '
                           'AND `dm`.`user_id` =? '
                           'JOIN `group` as `g` '
                           'ON `g`.`id` = `d`.`group_id` '
                           'WHERE `d`.`id` =?', (user_id, deadline_id))
            
            result = self._fetch_dict(cursor)
            deadline = self._create_entity(data=result)
            deadlineMeta = None
            if result['deadline_id']:
                deadlineMeta = DeadlineMetadata()
                deadlineMeta.user_id = result['user_id']
                deadlineMeta.deadline_id = result['deadline_id']
                deadlineMeta.notes = result['notes']
            deadline.meta = deadlineMeta
            return deadline

    def deadlines_in_group_with_same_name(self, deadline):
        deadline_list = []
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `d`.`id`, `d`.`name`, `d`.`group_id`, `d`.`deadline`, `d`.`type`, `dm`.`user_id`, `dm`.`deadline_id`, `dm`.`notes`, `g`.`name` as `group` '
                           'FROM `deadline` AS `d` '
                           'JOIN `group` as `g` '
                           'ON `g`.`id` = `d`.`group_id` '
                           'JOIN `deadline_metadata` as `dm` '
                           'ON `dm`.`deadline_id` = `d`.`id` '
                           'WHERE `d`.`name` =? '
                           'and `g`.`id` =?', (deadline.name,deadline.group_id))
            for result in self._fetch_all_dict(cursor):
                deadline = self._create_entity(data=result)
                deadlineMeta = None
                if result['user_id']:
                    deadlineMeta = DeadlineMetadata()
                    deadlineMeta.user_id = result['user_id']
                    deadlineMeta.deadline_id = result['id']
                    deadlineMeta.notes = result['notes']
                deadline.meta = deadlineMeta
                deadline_list.append(deadline)
        return deadline_list

    def perform_aggregation(self, deadline):
        candidates = self.deadlines_in_group_with_same_name(deadline)
        candidates_dates = [ deadline.deadline for deadline in candidates]
        gr = GroupRepository()
        threshold = math.ceil(gr.get_group_size(deadline.group_id) / 3)
        dmr = DeadlineMetadataRepository()

        print "Dates: " + str(candidates_dates)
        print "Threshold: " + str(threshold)
        print "Should Aggregate? " + str(should_aggregate(candidates_dates, threshold))

        if deadline.type == 'END':
            print "Performing Aggregation for Endorsed Deadline."
            for candidate in candidates:
                if candidate.meta:
                    candidate.meta.deadline_id = deadline.id
                    dmr.persist(candidate.meta)


        elif should_aggregate(candidates_dates, threshold):
            print "Aggregating for general deadline."
            canonical = deadline
            for candidate in candidates:
                if candidate.type == 'END':
                    deadline.meta.deadline_id = candidate.id
                    dmr.persist(deadline.meta)
                    canonical = candidate

            if canonical != deadline:
                canonical.meta = deadline.meta
            else:
                deadline.type = 'COM'
                for candidate in candidates:
                    if candidate.meta:
                        candidate.meta.deadline_id = deadline.id
                        dmr.persist(candidate.meta)
                self.raw_persist(deadline, False)
                
            deadline = canonical
            
        self.cleanup_orphan_deadlines()
        return deadline
    
    def cleanup_orphan_deadlines(self):
        with self._conn.cursor() as cursor:
            cursor.execute('DELETE FROM `deadline` '
                           'WHERE `id` NOT IN '
                           '(SELECT `deadline_id` FROM `deadline_metadata`) ')

    def _fetch_deadline(self, cursor):
        result = self._fetch_dict(cursor)
        if result is not None:
            return self._create_entity(data=result)
