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
                               '(`id`, `email`, `name`, `password`, `salt`) '
                               'VALUES (?, ?, ?, ?, ?)',
                               (cursor.lastrowid, delta['email'], delta['name'],
                                delta['password'], delta['salt']))
                
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

    def _update_group_membership(self, user):
        if not user.groups:
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
            cursor.execute('SELECT `id`, `email`, `name`, `password`, `salt` '
                           'FROM `user`'
                           'WHERE `id`=?', (user_id,))
            return self._fetch_user(cursor)

    def fetch_all(self):
        user_list = []
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `id`, `email`, `name`, `password`, `salt` '
                           'FROM `user`')
            for result in self._fetch_all_dict(cursor):
                user_list.append(self._create_entity(data=result))

        return user_list
        
    def get_user_by_email(self, email):
        with self._conn.cursor() as cursor:
            cursor.execute('SELECT `id`, `email`, `name`, `password`, `salt` '
                           'FROM `user`'
                           'WHERE `email`=?', (email,))
            return self._fetch_user(cursor)

    def _fetch_user(self, cursor):
        result = self._fetch_dict(cursor)
        if result is not None:
            return self._create_entity(data=result)
