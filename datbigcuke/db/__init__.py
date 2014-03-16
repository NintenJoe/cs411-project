"""Provide database connections."""

from __future__ import print_function
import tornado.options

_parse_config = lambda path: tornado.options.parse_config_file(path, final=False)

# module level options
tornado.options.define('db_config', type=str, callback=_parse_config)
tornado.options.define('mysql_provider', default='db.conn.mysql', type=str)
tornado.options.define('mysql_username', type=str)  # required
tornado.options.define('mysql_password', type=str)  # required

# enforce required options
def _options_check():
  options = tornado.options.options.as_dict()
  required_options = ['mysql_provider', 'mysql_username', 'mysql_password']
  for opt in required_options:
    if options[opt] is None:
      raise tornado.options.Error("required option '{}' is missing".format(opt))


tornado.options.add_parse_callback(_options_check)
