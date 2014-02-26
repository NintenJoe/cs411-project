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
from Application import Application

### Primary Entry Point ###

##  The primary entry point function for the CS411 project backend, which 
#   instantiates the backend to listen for API requests.
def main():
    # Global Option Configuration #
    tornado.options.define( "listen_port", default=9999,
                            help="Server Listen Port", type=int )
    tornado.options.define( "listen_address", default='',
                            help="Server Listen Address", type=str )

    # Start-Up Logic #
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer( Application() )
    server.listen( tornado.options.options.listen_port,
		   address=tornado.options.options.listen_address )
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
