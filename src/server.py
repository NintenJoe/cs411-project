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
import db
from Application import Application

# Global Option Configuration #
_parse_config = lambda path: tornado.options.parse_config_file(path, final=False)
tornado.options.define( "config", callback=_parse_config,
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
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer( Application() )
    opts = tornado.options.options
    server.listen( opts.listen_port, address=opts.listen_address )
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
