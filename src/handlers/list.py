# -*- coding: utf-8 -*-

from pagemanage.src.libs.handler import BaseHandler
from pagemanage.src.libs import cache

class ListHandler(BaseHandler):
    _handler_template = "views/page/list.html"
    
    @cache.cache()
    def product_list(self):
        return 'poduct list ent'
    
    def get(self):                
        self._context.title = "List"
        product_list = self.product_list()
        self.render(self._handler_template, product=product_list)

handlers = [
            (r"/list", ListHandler),
            ]
