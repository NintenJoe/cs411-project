"""Provide database connections."""

__author__ = 'Eunsoo Roh'
__copyright__ = 'Copyright 2014 Bigdatcuke Project'
__email__ = 'roh7@illinois.edu'


import tornado.options
import importlib


_parse_config = lambda path: tornado.options.parse_config_file(path, final=False)

# module level options
tornado.options.define('db_config', type=str, callback=_parse_config)
tornado.options.define('mysql_provider', default='db.conn.mysql', type=str)
tornado.options.define('mysql_hostname', default='localhost', type=str)
tornado.options.define('mysql_port', default=3306, type=int)
tornado.options.define('mysql_username', type=str)  # required
tornado.options.define('mysql_password', type=str)  # required
tornado.options.define('mysql_database', type=str)

# enforce required options
def _options_check():
  options = tornado.options.options.as_dict()
  required_options = ['mysql_username', 'mysql_password']
  for opt in required_options:
    if options[opt] is None:
      raise tornado.options.Error("required option '{}' is missing".format(opt))


tornado.options.add_parse_callback(_options_check)


class ProviderError(Exception):
  pass


def mysql_connect(provider=None, hostname=None, port=None,
                  username=None, password=None, database=None):
  """Connect to MySQL server using given provider."""
  provider = provider or tornado.options.options.mysql_provider
  hostname = hostname or tornado.options.options.mysql_hostname
  port = port or tornado.options.options.mysql_port
  username = username or tornado.options.options.mysql_username
  password = password or tornado.options.options.mysql_password
  database = database or tornado.options.options.mysql_database

  # get class or callable object from module
  try:
    module_name, attrib_name = provider.rsplit('.', 1)
    module = importlib.import_module(module_name)
    factory = getattr(module, attrib_name)
  except ImportError, AttributeError:
    raise ProviderError("cannot find requested provider '{}'".format(provider))

  return factory(hostname=hostname, port=port,
                 username=username, password=password, database=database)
