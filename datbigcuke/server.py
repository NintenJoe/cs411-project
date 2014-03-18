##  @file server.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Main Script for the CS411 Project Server
#
#   @TODO
#   - Add any supplemental Tornado configuration options within this file
#     as needed.

import tornado.httpserver
import tornado.options
import tornado.ioloop
import tornado.web
import sys
import datbigcuke.db
from datbigcuke.Application import Application

# Global Option Configuration #
_config_parsed = False
def _parse_config(path):
    _config_parsed = True
    tornado.options.parse_config_file(path, final=False)

tornado.options.define( "config", default='config/server.conf',
                        callback=_parse_config,
                        help="Master configuration file", type=str )
tornado.options.define( "listen_port", default=9999,
                        help="Server Listen Port", type=int )
tornado.options.define( "listen_address", default='',
                        help="Server Listen Address", type=str )
### Primary Entry Point ###

##  The primary entry point function for the CS411 project backend, which 
#   instantiates the backend to listen for API requests.
def main():
    # Start-Up Logic #
    try:
        tornado.options.parse_command_line(final=False)
        # this is a hack; we want to automatically load default config file before
        # validation is triggered with callbacks. However, while _parse_config is
        # triggered if --config is supplied, it is not triggered otherwise.
        # Since there is currently no other way to manually trigger it, force
        # trigger parsing if parse did not happen, then parse command line
        # again to make sure explicit command line arguments correctly overrides
        # the default settings.
        if _config_parsed:
            # everything is good; just trigger the callbacks
            tornado.options.parse_command_line([sys.argv[0]], final=True)
        else:
            _parse_config(tornado.options.options.config)
            tornado.options.parse_command_line()

    except tornado.options.Error as e:
        print >> sys.stderr, 'Error:', e
        tornado.options.print_help()
        return

    server = tornado.httpserver.HTTPServer( Application() )
    opts = tornado.options.options
    server.listen( opts.listen_port, address=opts.listen_address )
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
