"""Module for abstract entities."""

__author__ = 'Eunsoo Roh'
__copyright__ = 'Copyright 2014 Bigdatcuke Project'
__email__ = 'roh7@illinois.edu'


class Error(Exception):
    pass


class InvalidatedEntityError(Error):
    pass


class AbstractEntity(object):
    _ATTRIB_TO_DATA = {}

    def __init__(self, data=None):
        self.__data = data or {}

    def __getattr__(self, name):
        if name not in self._ATTRIB_TO_DATA:
            raise AttributeError(name)
        # if database source exists, use it
        key = self._ATTRIB_TO_DATA[name]
        return self.__data.get(key, None)

    def __setattr__(self, name, value):
        if name in self._ATTRIB_TO_DATA:
            # see whether this rolls back any previous changes
            key = self._ATTRIB_TO_DATA[name]
            if key in self.__data and value == self.__data[key]:
                if name in self.__dict__:
                    super(AbstractEntity, self).__delattr__(name)
                # return here so we don't add the attribute back
                return

        super(AbstractEntity, self).__setattr__(name, value)

    def __getattribute__(self, name):
        attrib = super(AbstractEntity, self).__getattribute__(name)
        # whitelist to prevent infinite recursion
        if (name in ('_AbstractEntity__data', '_ATTRIB_TO_DATA')
            or self.__data is not None):
            return attrib
        else:
            raise InvalidatedEntityError()

    def validate(self):
        return True

    def invalidate(self):
        """Invalidate the entity object to prevent any further use."""
        self.__data = None

    def get_delta(self):
        delta = {}
        for attrib in self._ATTRIB_TO_DATA:
            if attrib in self.__dict__:
                delta[self._ATTRIB_TO_DATA[attrib]] = getattr(self, attrib)
        return delta

    def _get_fields(self):
        fields = []
        for attrib, field in self._ATTRIB_TO_DATA.items():
            fields.append((field, getattr(self, attrib)))
        return fields

    def __repr__(self):
        field_formatter = lambda (a, v): '{}={!r}'.format(a, v)
        field_repr = ','.join(map(field_formatter, self._get_fields()))
        return '{}({})'.format(self.__class__.__name__, field_repr)
