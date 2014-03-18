"""Module for User repository.

UserRepository offers access and persistence of User objects.
"""

__author__ = 'Eunsoo Roh'
__copyright__ = 'Copyright 2014 Bigdatcuke Project'
__email__ = 'roh7@illinois.edu'


from datbigcuke.entities.User import User
import datbigcuke.db
import operator


class EntityValidationError(Exception):
    pass


class UserRepository(object):

    def __init__(self):
        self._conn = datbigcuke.db.mysql_connect()

    def close(self):
        self._conn.close()

    def persist(self, user):
        if not user.validate():
            raise EntityValidationError(user)

        delta = user.get_delta()
        delta.pop('id', None)  # make sure id does not exist
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
                user_list.append(User(data=result))

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
            return User(data=result)

    def _fetch_dict(self, cursor, header=None):
        if header is None:
            header = map(operator.itemgetter(0), cursor.description)
        result = cursor.fetchone()
        if result is not None:
            return dict(zip(header, result))
        
    def _fetch_all_dict(self, cursor):
        header = map(operator.itemgetter(0), cursor.description)
        while True:
            result = self._fetch_dict(cursor, header)
            if result is None:
                break
            yield result
