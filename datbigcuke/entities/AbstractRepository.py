"""Module for repository base class."""

__author__ = 'Eunsoo Roh'
__copyright__ = 'Copyright 2014 Bigdatcuke Project'
__email__ = 'roh7@illinois.edu'


import collections
import datbigcuke.db
import operator
from datbigcuke.entities.User import User


class EntityValidationError(Exception):
    pass


class AbstractRepository(object):

    class ObjectCache(object):
        """Cache per object type"""
        __cache_dict = collections.defaultdict(dict)
        def __get__(self, instance, owner):
            return self.__cache_dict[instance._obj_type]

    _obj_cache = ObjectCache()

    def __init__(self, obj_type):
        self._conn = datbigcuke.db.mysql_connect()
        self._obj_type = obj_type
        self._cache = {}  # object cache

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

    def _create_entity(self, data):
        assert 'id' in data
        entity = self._obj_cache.get(data['id'], None)
        if not entity:
            entity = self._obj_type(data=data)
            self._obj_cache[data['id']] = entity
        return entity
