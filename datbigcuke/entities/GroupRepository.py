"""Module for Group repository.

GroupRepository offers access and persistence of Group objects.
"""

__author__ = 'Eunsoo Roh'
__copyright__ = 'Copyright 2014 Bigdatcuke Project'
__email__ = 'roh7@illinois.edu'


from datbigcuke.entities.User import User
from datbigcuke.entities.Group import Group
from datbigcuke.entities.AbstractRepository import AbstractRepository
import datbigcuke.db
import operator

# @TODO(halstea2) Add 'remove' method for deleting a user.

class GroupRepository(AbstractRepository):

    def __init__(self):
        super(GroupRepository, self).__init__(Group)

    def close(self):
        self._conn.close()

    def persist(self, group):
        super(GroupRepository, self).persist(group)

        delta = group.get_delta()
        delta.pop('id', None)  # make sure id does not exist
        if group.id is None:
            # new user object
            with self._conn.cursor() as cursor:
                cursor.execute('INSERT INTO `membership_entity` VALUES ()')
                # TODO(roh7): figure out whether it is worth using exception
                # i.e. is there a case this would be true where execute() does
                # not throw an exception itself?
                assert cursor.lastrowid != 0
                cursor.execute('INSERT INTO `group'
                               '(`id`, `name`, `description`, `type`) '
                               'VALUES (?, ?, ?, ?)',
                               (cursor.lastrowid, delta['name'],
                                delta['description'], delta['type']))
                
        else:
            # old user object
            if delta:
                assert 'id' not in delta
                keys = delta.keys()
                args = list(delta.values())
                args.append(group.id)
                query = ','.join('`{}`=?'.format(k) for k in keys)
                with self._conn.cursor() as cursor:
                    cursor.execute('UPDATE `group` '
                                   'SET {} WHERE `id`=?'.format(query),
                                   args)
            
    def fetch(self, group_id):
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `id`, `name`, `description`, `type` '
                           'FROM `group`'
                           'WHERE `id`=?', (group_id,))
            return self._fetch_group(cursor)

    def fetch_all(self):
        group_list = []
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `id`, `name`, `description`, `type` '
                           'FROM `group`')
            for result in self._fetch_all_dict(cursor):
                group_list.append(self._create_entity(data=result))

        return group_list

    def get_groups_of_user(self, user_id):
        group_list = []
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `g`.`id` AS `id`, `g`.`name` AS `name`,'
                           '`g`.`description` AS `description`, `g`.`type` AS `type`'
                           'FROM `group` AS `g`'
                           'JOIN `group_membership` AS `m`'
                           '    ON (`m`.`group_id` = `g`.`id`)'
                           'WHERE `m`.`member_id`=?', (user_id,))
            for result in self._fetch_all_dict(cursor):
                group_list.append(self._create_entity(data=result))

        return group_list
        
    def get_subgroups_of_group(self, group_id):
        group_list = []
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `g`.`id` AS `id`, `g`.`name` AS `name`,'
                           '`g`.`description` AS `description`, `g`.`type` AS `type`'
                           'FROM `group` AS `gr`'
                           'JOIN `group_membership` AS `m`'
                           '    ON (`m`.`group_id` = `gr`.`id`)'
                           'JOIN `group` AS `g`'
                           '    ON (`g`.`id` = `m`.`member_id`)'
                           'WHERE `gr`.`id` =?', (group_id,))
            for result in self._fetch_all_dict(cursor):
                group_list.append(self._create_entity(data=result))
            
        for group in group_list:
            group.subgroups = self.get_subgroups_of_group(group.id)
        return group_list

    def _fetch_group(self, cursor):
        result = self._fetch_dict(cursor)
        if result is not None:
            return self._create_entity(data=result)
