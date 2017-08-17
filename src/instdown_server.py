# !/usr/bin/env python
# -*- coding:utf-8 -*-
""" the instdown server.
"""
import libs.log
import libs.config
import tornado.httpserver
import tornado.netutil
import tornado.process
from tornado import web
from tornado import ioloop
from handlers.resource_handler import ResourceHandler
from handlers.index_handler import IndexHandler
import os
import sys

error_logger = libs.log.get_logger('error')
config = libs.config.get_config(conf='online.cfg')

def initialize(debug=False):
    """ Initialize something.
    """
    global application, config
    settings = {
        'debug': debug,
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }
    if debug:
        config = libs.config.get_config(conf='offline.cfg')
    application = web.Application([
        # ad handler
        (r'/instdown/resource', ResourceHandler),
        (r'/', IndexHandler),
        web.URLSpec(r"/(.*)", web.StaticFileHandler, {"path": "static"}),  
    ], **settings)


def start_server_mulp():
    """ the function to start server.
    """
    initialize()
    global config, application
    sockets = tornado.netutil.bind_sockets(config.get('server', 'port'))
    tornado.process.fork_processes(config.getint('server', 'process'))
    server = tornado.httpserver.HTTPServer(application)
    server.add_sockets(sockets)
    ioloop.IOLoop.instance().start()


def start_debug_server():
    """ the function to start server.
    """
    initialize(debug=True)
    global config, application
    sockets = tornado.netutil.bind_sockets(config.get('server', 'port'))
    server = tornado.httpserver.HTTPServer(application)
    server.add_sockets(sockets)
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        start_debug_server()
    else:
        start_server_mulp()

