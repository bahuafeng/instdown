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
            ip = self.request.remote_ip
            ua = self.request.headers.get("User-Agent")
            instagram_url = self.get_argument('url')
            resource_url = models.parser.parse(instagram_url)
        except Exception as e:
            ret = dict(
                errno = 1,
                errmsg = str(e),
                data = None,
            )
            logger.error('error', e)
        else:
            ret = dict(
                errno = 0,
                errmsg = 'success',
                data = resource_url
            )
            logger.info(
                url=instagram_url,
                resource_url=resource_url,
                ip=ip, ua=ua)
        finally:
            self.write(json.dumps(ret))

