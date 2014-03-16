"""MySQL connection factory module.

This module currently only provides abstraction over connection instantiation.

@TODO(roh7): implement wrapper class for consistent abstraction
"""

def _translate_keys(dictionary, translation):
  for key_from, key_to in translation.items():
    if key_from in dictionary:
      dictionary[key_to] = dictionary.pop(key_from)


def mysqldb(**kwargs):
  """Create MySQL connection using MySQLdb library."""
  import MySQLdb
  # translate keyword arguments
  translation = { 'hostname': 'host',
                  'username': 'user',
                  'password': 'passwd',
                  'database': 'db',
                }
  _translate_keys(kwargs, translation)

  return MySQLdb.connect(**kwargs)


def oursql(**kwargs):
  """Create MySQL connection using oursql library."""
  import oursql
  translation = { 'hostname': 'host',
                  'username': 'user',
                  'password': 'passwd',
                  'database': 'db',
                }
  _translate_keys(kwargs, translation)
  return oursql.connect(**kwargs)
