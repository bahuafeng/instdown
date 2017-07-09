#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Query Handler
"""
import tornado.web
import json
import libs.log
import models.parser

class ResourceHandler(tornado.web.RequestHandler):
    """Query Handler
    """
    
    def get(self):
        """GET method
        """
        logger = libs.log.get_logger('resource')
        try:
            instagram_url = self.get_argument('url')
            resource_url = models.parser.parse(instagram_url)
        except Exception as e:
            ret = dict(
                errno = 1,
                errmsg = str(e),
                data = None,
            )
        else:
            ret = dict(
                errno = 0,
                errmsg = 'success',
                data = resource_url
            )
        finally:
            self.write(json.dumps(ret))

