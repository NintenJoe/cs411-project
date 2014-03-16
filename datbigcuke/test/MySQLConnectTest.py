"""Test for db.mysql_connect() function."""

import unittest
import datbigcuke.db
import tornado.options
import mock


# parameters for testing
DEFAULT_PROVIDER=__name__+'.fake_provider'
DEFAULT_HOSTNAME='mysql.datbigcuke.com'
DEFAULT_PORT=16384
DEFAULT_USERNAME='cukumber'
DEFAULT_PASSWORD='hugh?'
DEFAULT_DATABASE='to_data_or_not_to_data'
# the following set should be different from above settings
OVERRIDE_PROVIDER=__name__+'.fake_provider_override'
OVERRIDE_HOSTNAME='dat.cuke.com'
OVERRIDE_PORT=12345
OVERRIDE_USERNAME='no'
OVERRIDE_PASSWORD='pwd'
OVERRIDE_DATABASE='nondefault'


# fake connection providers for testing
def fake_provider(**kwargs):
  kwargs['override'] = False
  return kwargs


def fake_provider_override(**kwargs):
  result = fake_provider(**kwargs)
  result['override'] = True
  return result


class MySQLConnectTest(unittest.TestCase):
  def setUp(self):
    patcher = mock.patch.multiple(tornado.options.options.mockable(),
                                  mysql_provider=DEFAULT_PROVIDER,
                                  mysql_hostname=DEFAULT_HOSTNAME,
                                  mysql_port=DEFAULT_PORT,
                                  mysql_username=DEFAULT_USERNAME,
                                  mysql_password=DEFAULT_PASSWORD,
                                  mysql_database=DEFAULT_DATABASE)
    mock_options = patcher.start()
    self.addCleanup(patcher.stop)

  def test_default(self):
    result = datbigcuke.db.mysql_connect()
    expected = { 'override': False, 'hostname': DEFAULT_HOSTNAME,
                 'port': DEFAULT_PORT, 'username': DEFAULT_USERNAME,
                 'password': DEFAULT_PASSWORD, 'database': DEFAULT_DATABASE }
    self.assertEquals(expected, result)

  def test_override(self):
    result = datbigcuke.db.mysql_connect(provider=OVERRIDE_PROVIDER,
                                         hostname=OVERRIDE_HOSTNAME,
                                         port=OVERRIDE_PORT,
                                         username=OVERRIDE_USERNAME,
                                         password=OVERRIDE_PASSWORD,
                                         database=OVERRIDE_DATABASE)
    expected = { 'override': True, 'hostname': OVERRIDE_HOSTNAME,
                 'port': OVERRIDE_PORT, 'username': OVERRIDE_USERNAME,
                 'password': OVERRIDE_PASSWORD, 'database': OVERRIDE_DATABASE }
    self.assertEquals(expected, result)
