#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
os.environ["PYTHON_EGG_CACHE"] = "/tmp/egg"

import tornado
from tornado import web
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import options

try:
    import pagemanage
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from pagemanage.src.libs.utils import parse_config_file

class Application(web.Application):
    def __init__(self):
        from pagemanage.urls import handlers, sub_handlers, ui_modules

        settings = dict(
            debug=options.debug,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=options.xsrf_cookies,
            cookie_secret=options.cookie_secret,
            login_url=options.login_url,
            static_url_prefix=options.static_url_prefix,

            ui_modules=ui_modules,
        )
        super(Application, self).__init__(handlers, **settings)

        # add handlers for sub domains
        for sub_handler in sub_handlers:
            # host pattern and handlers
            self.add_handlers(sub_handler[0], sub_handler[1])

def main(port=0):    
    parse_config_file("/Users/andy/Sites/pagemanage/pagemanage.conf")
    tornado.options.parse_command_line()

    http_server = HTTPServer(Application(), xheaders=True)
    port = port if port else options.port
    num_processes = options.num_processes

    if options.debug:
        num_processes = 1
    
    http_server.bind(int(port))
    http_server.start(int(num_processes))

    IOLoop.instance().start()

if __name__ == "__main__":    
    try:
        port = int(sys.argv[1])
    except Exception:
        port = 0
    main(port)    