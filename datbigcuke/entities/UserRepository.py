"""Module for User repository.

UserRepository offers access and persistence of User objects.
"""

__author__ = 'Eunsoo Roh'
__copyright__ = 'Copyright 2014 Bigdatcuke Project'
__email__ = 'roh7@illinois.edu'


from datbigcuke.entities.User import User
from datbigcuke.entities.AbstractRepository import AbstractRepository
import datbigcuke.db
import operator


class UserRepository(AbstractRepository):

    def __init__(self):
        super(UserRepository, self).__init__(User)

    def persist(self, user):
        super(UserRepository, self).persist(user)

        delta = user.get_delta()
        delta.pop('id', None)  # make sure id does not exist
        # TODO(roh7): improve delta handling for iterables
        delta.pop('groups', None)  # make sure id does not exist
        if user.id is None:
            # new user object
            with self._conn.cursor() as cursor:
                cursor.execute('INSERT INTO `membership_entity` VALUES ()')
                # TODO(roh7): figure out whether it is worth using exception
                # i.e. is there a case this would be true where execute() does
                # not throw an exception itself?
                assert cursor.lastrowid != 0
                cursor.execute('INSERT INTO `user`'
                               '(`id`, `email`, `name`, `password`, `salt`, `confirmUUID`) '
                               'VALUES (?, ?, ?, ?, ?, ?); ',
                               (cursor.lastrowid, delta['email'], delta['name'],
                                delta['password'], delta['salt'], delta['confirmUUID']))
                cursor.execute('SELECT `id`, `email`, `name`, `password`, `salt`, `refreshTok` '
                               'FROM `user`'
                               'WHERE `id`=LAST_INSERT_ID()')
                user = self._fetch_user(cursor)
                
        else:
            # old user object
            if delta:
                assert 'id' not in delta
                keys = delta.keys()
                args = list(delta.values())
                args.append(user.id)
                query = ','.join('`{}`=?'.format(k) for k in keys)
                with self._conn.cursor() as cursor:
                    cursor.execute('UPDATE `user` '
                                   'SET {} WHERE `id`=?'.format(query),
                                   args)

        self._update_group_membership(user)
        return user

    def remove(self, user):
        with self._conn.cursor() as cursor:
            cursor.execute('DELETE FROM `membership_entity` WHERE `id`=?',
                           (user.id,))
            user.invalidate()

    def _update_group_membership(self, user):
        if user.groups is None:
            return

        # TODO(roh7): reconsider whether this is the right place
        with self._conn.cursor() as cursor:
            cursor.execute('DELETE FROM `group_membership`'
                           'WHERE `member_id`=?', (user.id,))
            cursor.executemany('INSERT INTO `group_membership`'
                               '(`group_id`, `member_id`)'
                               'VALUES (?,?)',
                               ((gid, user.id) for gid in user.groups))

    def fetch(self, user_id):
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `id`, `email`, `name`, `password`, `salt`, `refreshTok` '
                           'FROM `user`'
                           'WHERE `id`=?', (user_id,))
            return self._fetch_user(cursor)

    def fetch_all(self):
        user_list = []
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `id`, `email`, `name`, `password`, `salt`, `refreshTok` '
                           'FROM `user`')
            user_list = self._fetch_all_users(cursor)

        return user_list
        
    def get_user_by_email(self, email):
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `id`, `email`, `name`, `password`, `salt`, `confirmed`, `refreshTok` '
                           'FROM `user`'
                           'WHERE `email`=?', (email,))
            return self._fetch_user(cursor)

    def get_members_of_group(self, group_id):
        member_list = []
        print "Group id: ", group_id
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `u`.`id`, `u`.`email`, `u`.`name`, `u`.`password`, `u`.`salt`, `u`.`confirmed` , `u`.`refreshTok`'
                           'FROM `group` AS `gr`'
                           'JOIN `group_membership` AS `m`'
                           '    ON (`m`.`group_id` = `gr`.`id`)'
                           'JOIN `user` AS `u`'
                           '    ON (`u`.`id` = `m`.`member_id`)'
                           'WHERE `gr`.`id` =? '
                           'ORDER BY `u`.`name`', (group_id,))
            member_list = self._fetch_all_users(cursor)
        
        return member_list

    # TODO(ciurej2): Why was this necessary to have a groups field here?
    def add_user_to_group(self, user, group):
        with self._conn.cursor() as cursor:
            cursor.execute('INSERT INTO `group_membership` (`group_id`, `member_id`) '
                           'VALUES (?,?)', (group.id, user.id))
        if user.groups:
            user.groups.append(group.id)

    def mark_verified(self, unique):
        with self._conn.cursor() as cursor:
            cursor.execute('UPDATE `user` '
                           'SET confirmed = true '
                           'WHERE `confirmUUID`=?', (unique,))

    def find_users_with_email_prefix(self, user_id, supergroup_id, prefix):
        user_list = []

        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `u`.`id`, `u`.`email`, `gm`.`group_id`'
                           'FROM `user` AS `u`'
                           'JOIN `group_membership` AS `gm`'
                           'ON `u`.`id` = `gm`.`member_id`'
                           'WHERE `gm`.`group_id`=? AND `u`.`email` LIKE ?',
                           (supergroup_id, '{!s}%'.format(prefix)))

            for result in self._fetch_all_dict(cursor):
                user_list.append(self._create_entity(data=result))

        return user_list

    def _fetch_user_groups(self, cursor, user_id):
        group_list = []
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `g`.`id` AS `id`'
                           'FROM `group` AS `g`'
                           'JOIN `group_membership` AS `m`'
                           '    ON (`m`.`group_id` = `g`.`id`)'
                           'WHERE `m`.`member_id`=?', (user_id,))
            for result in self._fetch_all_dict(cursor):
                group_list.append(result['id'])

        return group_list

    def _fetch_user(self, cursor):
        result = self._fetch_dict(cursor)
        if not result:
            return None

        result['groups'] = self._fetch_user_groups(cursor, result['id'])
        user = self._create_entity(data=result)
        return user

    def _fetch_all_users(self, cursor):
        user_list = []
        for result in self._fetch_all_dict(cursor):
            result['groups'] = self._fetch_user_groups(cursor, result['id'])
            user_list.append(self._create_entity(data=result))
        return user_list
