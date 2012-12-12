# -*- coding: utf-8 -*-

from tornado.options import options

from pagemanage.src.libs.handler import BaseHandler

_template_path = "views/item"

class DetailHandler(BaseHandler):
    def get(self, code):        
        self.render("%s/detail.html" % _template_path)
        
class LoveHandler(BaseHandler):
    def get(self,code):
        self.render("%s/love.html" % _template_path)

class MaybeHandler(BaseHandler):
    def get(self, code):
        self.render("%s/maybe.html" % _template_path)
                
handlers = [
            (r"/item/([0-9a-zA-Z\-\_\+]+)/love", LoveHandler),
            (r"/item/([0-9a-zA-Z\-\_\+]+)/maybe", MaybeHandler),
            (r"/item/([0-9a-zA-Z\-\_\+]+)", DetailHandler),            
            ]