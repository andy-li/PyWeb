# -*- coding: utf-8 -*-

import os
import hashlib

from tornado.options import define, options

class _NoDefault:
    """No default value rather than confused None"""
    def __repr__(self):
        return '(No Default)'
    
NoDefault = _NoDefault()

def find_modules(modules_dir):
    try:
        return [f[:-3] for f in os.listdir(modules_dir)
                if not f.startswith('_') and f.endswith('.py')]
    except OSError:
        return []
    
def parse_config_file(path):
    """Rewrite tornado default parse_config_file.
    
    Parses and loads the Python config file at the given path.
    
    This version allow customize new options which are not defined before
    from a configuration file.
    """
    config = {}
    execfile(path, config, config)
    for name in config:
        if name in options:
            options[name].set(config[name])
        else:
            define(name, config[name])

def hash_password(passwd):
        
    key = options.password_key                
    assert isinstance(key, str)
    assert isinstance(passwd, str)

    key = key[:8]
    result = passwd + key
    md5 = hashlib.md5()
    md5.update(result)
    result = md5.hexdigest()

    password = ''    
    for i in xrange(0,31):
        if i % 2 == 0:
            password = password + result[i]
                
    return password

def pagevar(page):
    try:
        page = int(page)
        if page < 1:
            page = 1
    except Exception:
        page = 1
    
    return page