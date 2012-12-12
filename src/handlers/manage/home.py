# -*- coding: utf-8 -*-

from tornado.options import options

from pagemanage.src.libs.handler import AdminBaseHandler

class AdminHomeHandler(AdminBaseHandler):
    def get(self):
        
        self._context.title = "控制台首页"
        self.render('admin/home.html')

handlers = [
            (r"%s/home" % options.admin_url, AdminHomeHandler),
            ]
