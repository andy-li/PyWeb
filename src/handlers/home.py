# -*- coding: utf-8 -*-

from tornado.web import UIModule

from pagemanage.src.libs.handler import BaseHandler
from pagemanage.src.libs import cache

class HomeHandler(BaseHandler):
    _handler_template = "views/page/index.html"
    
    @cache.cache()
    def product_list(self):
        return 'poduct list ent'
    
    def get(self):                
        self._context.title = "Home"
        product_list = self.product_list()
        self.render(self._handler_template, product=product_list)

class WebsitesModule(UIModule):
    def render(self, page):
        return self.render_string("modules/websites.html", page=page)

handlers = [
            (r"/", HomeHandler),
            ]

ui_modules = {
              "websites":WebsitesModule,
              }