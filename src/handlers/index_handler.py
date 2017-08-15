#-*- coding:utf-8 -*-  
#!/usr/bin/python  

"""
File Name: index_handler.py
Author: bahuafeng
Mail: bahuafeng@gmail.com  
Created Time: 2017-07-23 23:05:10
Brief: TODO
"""

import tornado.web
import libs.log

class IndexHandler(tornado.web.RequestHandler):
    """ index page
    """
    def get(self):
        logger = libs.log.get_logger('index')
        instdown_api = "/instdown/resource"
        ip = self.request.remote_ip
        ua = self.request.headers.get("User-Agent")
        self.render("../template/index.html", instdown_api=instdown_api)
        logger.info(ip=ip, ua=ua)
