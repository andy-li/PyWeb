# -*- coding: utf-8 -*-

from pagemanage.src.libs.handler import ErrorHandler 

handlers = []
sub_handlers = []
ui_modules = {}

from pagemanage.src.handlers import home,auth,about, item, \
                                    list, people, \
                                    admin

handlers.extend(home.handlers)
handlers.extend(auth.handlers)
handlers.extend(about.handlers)
handlers.extend(item.handlers)
handlers.extend(list.handlers)
handlers.extend(people.handlers)

handlers.extend(admin.handlers)

# Append default 404 handler, and make sure it is the last one.
handlers.append((r".*", ErrorHandler))

ui_modules.update(home.ui_modules)
ui_modules.update(admin.ui_modules)

for sh in sub_handlers:
    sh.append((r".*", ErrorHandler))