# -*- coding: utf-8 -*-

import logging
from formencode import validators
from tornado.options import options

from pagemanage.src.forms.base import BaseForm, URL
from pagemanage.src.model.members import Member
from pagemanage.src.libs.utils import hash_password

class LoginForm(BaseForm):
    email = validators.Email(not_empty=True, resolve_domain=False, max=120, strip=True)
    auth_passwd = validators.PlainText(not_empty=True, strip=True, messages={'empty':u'请输入登录密码'})    
    
    next = validators.String(not_empty=False, max=600)
    
    def __after__(self):
        try:
            v = self._values
            email = v['email']
            
            member = Member().findby_email(email)
            if not member:
                self.add_error('email', u"Email与密码不匹配。")
            else:   
                passwd = hash_password(v['auth_passwd'])
                if member['hash_password'] != passwd:
                    self.add_error('email', u"Email与密码不匹配。")
                elif not member['verify']:
                    self.add_error('email', u"您的Email未通过验证，无法登录。")               
                                                                                
        except Exception, e:
            logging.error(str(e))
            self.add_error("email", u"登录失败，请稍后重试。")
            
class RegisterForm(BaseForm):
    email = validators.Email(not_empty=True, resolve_domain=False, max=120, strip=True)
    nickname = validators.String(not_empty=True, max=32, strip=True, messages={'empty':u'请给自己取个昵称。'})
    auth_passwd = validators.PlainText(not_empty=True, messages={'empty':u'请输入一个密码，用于登录。'})
    auth_repasswd = validators.PlainText(not_empty=True, messages={'empty':u'请输入重复密码'})
    chained_validators=[validators.FieldsMatch('auth_passwd','auth_repasswd', messages={'invalidNoMatch':u'两次密码输入不一致'})]
    
    next = validators.String(not_empty=False, max=600)
    
    def __after__(self):
        try:
            v = self._values
            email = v['email']            
            nickname = v['nickname']
            passwd = v['auth_passwd']
                                    
            if len(nickname) < 2:
                self.add_error('nickname', u"昵称至少需要两个字。")
            elif len(passwd) < 6:
                self.add_error('auth_passwd', u"安全起见，密码至少需要六位。")   
            else:
                has = Member().findby_email(email)                  
                if has:
                    self.add_error('email', u"Email已经被使用，请尝试换个Email地址。")
                else:               
                    Member().insert_new(email=email, nickname=nickname, hash_password=hash_password(passwd))
                                                 
        except Exception, e:
            logging.error(str(e))
            self.add_error("email", u"注册失败，请稍后重试。")

class ResetForm(BaseForm):
    email = validators.Email(not_empty=True, resolve_domain=False, max=120, strip=True)
    
    def __after__(self):
        try:
            email = self._values['email']
            if not Member().findby_email(email):
                self.add_error('email', u"邮箱地址未被使用。")
        except Exception, e:
            logging.error(str(e))
            self.add_error("email", u"重置密码失败，请重试。")
            
class VerifyResetForm(BaseForm):
    auth_passwd = validators.PlainText(not_empty=True, messages={'empty':u'请输入新的密码'})
    auth_repasswd = validators.PlainText(not_empty=True, messages={'empty':u'请输入重复密码'})
    chained_validators=[validators.FieldsMatch('auth_passwd','auth_repasswd', messages={'invalidNoMatch':u'两次密码输入不一致'})]
    
    code = validators.String(not_empty=True, max=100)
    co = validators.String(not_empty=True, max=200)
    
    def __after__(self):
        passwd = self._values['auth_passwd']
        if len(passwd) < 6:
            self.add_error('auth_passwd', u"安全起见，密码至少需要六位。") 
        else:
            try:
                Member().reset_passwd(email=self._values['co'], new_hash_password=hash_password(passwd))
            except Exception,e:
                logging.error(str(e))
                self.add_error("auth_passwd", u"重置密码失败，请重试。")
    