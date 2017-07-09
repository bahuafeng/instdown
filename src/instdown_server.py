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

error_logger = libs.log.get_logger('error')
config = libs.config.get_config()


def initialize(debug=False):
    """ Initialize something.
    """
    global application
    settings = {
            'debug': debug,
            }
    application = web.Application([
        # ad handler
        (r'/instdown/res', CateADHandler, dict(log=cate_ad_logger, root_log=root_logger)),
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
    sockets = tornado.netutil.bind_sockets(config.get('server_debug', 'port'))
    server = tornado.httpserver.HTTPServer(application)
    server.add_sockets(sockets)
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        start_debug_server()
    else:
        start_server_mulp()

