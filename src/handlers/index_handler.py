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

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        instdown_api = "/instdown/resource"
        self.render("../template/index.html", instdown_api=instdown_api)
