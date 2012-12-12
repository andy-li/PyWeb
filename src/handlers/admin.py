# -*- coding: utf-8 -*-

import math

from tornado.web import UIModule
from tornado.options import options

from pagemanage.src.libs.handler import AdminBaseHandler

from pagemanage.src.handlers.manage import home, product

class AdminMainHandler(AdminBaseHandler):
    def get(self):
        self.render('admin/main.html')        

class AdminHeadHandler(AdminBaseHandler):
    def get(self):
        self.render('admin/head.html')

class SidebarModule(UIModule):
    def render(self, cur_page=''):
        return self.render_string("admin/sidebar.html", \
                                  cur_page=cur_page)
class PagerModule(UIModule):    
    def render(self, num, page, url, pagesize, args):
        try:
            url = str(url)
            num = int(num)
            page = int(page)
            pagesize = int(pagesize)
        except Exception:
            return ''
                
        if args:
            for k in args:
                url += '&' if url.find('?') > -1 else '?'
                url += str(k) + '=' + str(args[k])
                
        url += '&' if url.find('?') > -1 else '?'
        url += 'page='
        
        if pagesize < 1: pagesize = 10
        if num < pagesize: return ''
        if page < 1: page = 1
                        
        pagecount = int(math.ceil(math.floor(num) / math.floor(pagesize)))
        breakspace = 10        
        
        pager = ""
        
        mp = page % breakspace
        if mp > 0:
            fr = page / breakspace * breakspace            
            to = (page / breakspace + 1) * breakspace
        else:
            fr = page - breakspace
            to = page if page > breakspace else breakspace
        if to > pagecount: to = pagecount
        
        pager += u"<li class='info'>%s / %s页</li>" % (str(page), str(pagecount))
        
        if page > 1:
            pager += u"<li><a href='%s%s'>首页</a></li>" % (url, str(1))
            pager += u"<li><a href='%s%s'>上一页</a></li>" % (url, str(page-1))            
        for i in range(fr+1, to+1):
            if page == i:
                pager += u"<li><a href='%s%s' class='on'>%s</a></li>" % (url, str(i), str(i))
            else:
                pager += u"<li><a href='%s%s'>%s</a></li>" % (url, str(i), str(i))                            

        if page < pagecount:
            pager += u"<li><a href='%s%s'>下一页</a></li>" % (url, str(page+1))
            pager += u"<li><a href='%s%s'>尾页</a></li>" % (url, str(pagecount))                        
        
        return pager

handlers = [
            (r"%s" % options.admin_url, AdminMainHandler),
            (r"%s/head" % options.admin_url, AdminHeadHandler),
            ]

ui_modules = {
              "Admin_sidebar" : SidebarModule,
              "Admin_pager" : PagerModule,
              }

handlers.extend(home.handlers)
handlers.extend(product.handlers)