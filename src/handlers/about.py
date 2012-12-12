# -*- coding: utf-8 -*-

from tornado.web import HTTPError

from pagemanage.src.libs.handler import BaseHandler
from pagemanage.src.libs import cache

from pagemanage.src.model.about import About

class AboutHandler(BaseHandler):
    _handler_template = "views/page/about.html"
    
    @cache.cache(expire=86400*7) #7 days
    def page_entry(self, page=""):
        if page == "":
            page = 'us'
        
        return About().findby_page(page)
    
    
    def get(self, page=""):                
        entry = self.page_entry(page)        
        if not entry: raise HTTPError(404)     
        
        self._context.title = entry['title']
        self._context.keywords = ",".join((entry['title'], self._context.keywords))
        self._context.description = ",".join((entry['title'], self._context.description))
        
        self.render(self._handler_template, entry=entry)
        
handlers = [(r"/about", AboutHandler),
            (r"/about/([a-z]{2,20})", AboutHandler),
            ]