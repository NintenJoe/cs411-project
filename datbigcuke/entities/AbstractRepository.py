"""Module for repository base class."""

__author__ = 'Eunsoo Roh'
__copyright__ = 'Copyright 2014 Bigdatcuke Project'
__email__ = 'roh7@illinois.edu'


from datbigcuke.entities.User import User
import datbigcuke.db
import operator


class EntityValidationError(Exception):
    pass


class AbstractRepository(object):

    def __init__(self, obj_type):
        self._conn = datbigcuke.db.mysql_connect()
        self._type = obj_type

    def close(self):
        self._conn.close()

    def persist(self, obj):
        if not obj.validate():
            raise EntityValidationError(user)
            
    def fetch(self, user_id):
        pass

    def fetch_all(self):
        pass

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
