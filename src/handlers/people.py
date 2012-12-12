# -*- coding: utf-8 -*-

from tornado.options import options

from pagemanage.src.libs.handler import BaseHandler

_template_path = "views/people"

class PeopleHandler(BaseHandler):
    def get(self, url):
        m = self.get_current_user()
        if m and m['nickname'] == url:
            self.render("%s/home.html" % _template_path)
        else:
            self.render("%s/people.html" % _template_path)
       
class LoveHandler(BaseHandler):
    def get(self):
        self.render("%s/love.html" % _template_path)

class SettingsHandler(BaseHandler):
    def get(self):
        self.render("%s/settings.html" % _template_path)   

class PeopleLoveHandler(BaseHandler):
    def get(self, url):
        self.render("%s/people-love.html" % _template_path)   
                 
handlers = [
            (r"/people/settings", SettingsHandler),
            (r"/people/love", LoveHandler),
            (r"/people/([0-9a-zA-Z\-\_\+]+)/love", PeopleLoveHandler),
            (r"/people/([0-9a-zA-Z\-\_\+]+)", PeopleHandler),            
            ]