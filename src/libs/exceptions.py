# -*- coding: utf-8 -*-

class BaseError(Exception):
    """Powered sites base exception"""
    pass

class DBConnectionError(BaseError):
    """Unable to connect to database"""
    pass

class DBAuthenticatedError(BaseError):
    """Authentication to database failed"""
    pass

class DBAttributeError(BaseError):
    pass

class TemplateContextError(BaseError):
    """Template context variable does not exist."""
    pass

class PageError(BaseError):
    pass