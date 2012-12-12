# -*- coding: utf-8 -*-

import re
import time

from tornado.options import options
from tornado import escape
from tornado.web import HTTPError

from pagemanage.src.libs.handler import BaseHandler
from pagemanage.src.forms.auth import LoginForm, RegisterForm, ResetForm, VerifyResetForm
from pagemanage.src.model.verify import Verify
from pagemanage.src.model.members import Member
from pagemanage.src.libs import mail

_template_path = "views/auth"

class SigninHandler(BaseHandler):    
    def get(self):                
        next = self.get_secure_cookie("next") 
        if not next:       
            next = self.get_argument("next", options.home_url)
        if next.startswith(options.login_url):
            self.redirect("/login")
            return
        
        self.clear_cookie("next")
        
        self._context.next = next
        self._context.title = u"登录"
        self.render("%s/sign-in.html" % _template_path)
    
    def post(self):        
        fm = LoginForm(self)                
        self._context.title = u"登录"
        self._context.next = escape.url_unescape(fm._parmas.get("next", "/"))
        if fm.validate():
            email = str(self.get_argument("email", ''))
            email.strip()
            
            self.login_in(email)                        
            
            auto_login = self.get_argument("auto_login", '')
            if auto_login:
                pass
            
            self.redirect(self._context.next)
        else:
            fm.render("%s/sign-in.html" % _template_path)        
            
class SignoutHandler(BaseHandler):    
    def get(self):
        self.login_out()
        self.redirect(self.get_argument("next", "/"))

class SignupHandler(BaseHandler):        
    def get(self):                
        next = self.get_argument("next", options.home_url)
        
        self._context.next = next
        self._context.title = u"注册"
        self.render("%s/sign-up.html" % _template_path)
        
    def post(self):
        fm = RegisterForm(self)
        self._context.title = u"注册"
        self._context.next = escape.url_unescape(fm._parmas.get("next", "/"))
        if fm.validate():
            self.set_secure_cookie('next', self._context.next)  
            
            nickname = self.get_argument("nickname", '')
            nickname.strip()
            email = self.get_argument("email", '')
            email.strip()                
            
            u"""发送注册验证邮件"""
            verify_url = send_verify_mail(self, 'signup', email, nickname)                    
            
            mail = re.compile(r'\@').split(email)
            mail_url = 'http://mail.%s' % mail[1]            
                      
            self._context.title = u"验证Email"            
            self.render("%s/sign-up-finish.html" % _template_path, \
                            email=email, mail_url=mail_url, \
                            nickname=nickname, verify_url=verify_url)                                    
        else:
            fm.render("%s/sign-up.html" % _template_path)

class VerifySignupHandler(BaseHandler):
    def get(self):        
        verify = self.chk_verify('signup')
        if not verify:
            return self.message('error', u'Email验证码校正失败')
        
        M = Member()
        member = M.findby_email(verify['content'])
        if not member:
            return self.message('error', u'Email验证码校正失败')
        else:                    
            M.update_verify(member['email'])
            Verify().remove(verify['_id'])
            self._context.title = u"Email验证成功！"
            self.render("%s/verify-signup.html" % _template_path, email=member['email'])

    def chk_verify(self, type):
        code = self.get_argument('code', False)
        email = self.get_argument('co', False)
        if not code or not email:
            return False          
        
        verify = Verify().findby_code(code)
        if not verify:
            return False
        elif verify['type'] != type:
            return False
        elif verify['content'] != email:
            return False
        elif verify['exptime'] < time.time():
            return False
        else:
            return verify      

class ResetHandler(BaseHandler):
    def get(self):
        self._context.title = u"重置密码"
        self.render("%s/sign-reset.html" % _template_path)
    
    def post(self):
        fm = ResetForm(self)
        if fm.validate():
            email = self.get_argument('email')
            member = Member().findby_email(email)
            u"""发送重置密码邮件"""  
            verify_url = send_verify_mail(self, 'reset', email, member['nickname'])
            
            mail = re.compile(r'\@').split(email)
            mail_url = 'http://mail.%s' % mail[1] 
            
            self.render("%s/sign-reset-finish.html" % _template_path, email=email, \
                        mail_url=mail_url, nickname=member['nickname'], verify_url=verify_url)
        else:
            fm.render("%s/sign-reset.html" % _template_path)

class VerifyResetHandler(VerifySignupHandler):    
    def get(self):       
        self._context.title = u"重置密码"
        self.render("%s/verify-reset.html" % _template_path, \
                    code=self.get_argument('code', ''), co=self.get_argument('co', ''))
        
    def post(self):
        verify =  self.chk_verify('reset')
        if not verify:
            return self.message('error', u'Email验证码校正失败。')
                
        fm = VerifyResetForm(self)
        if fm.validate():            
            Verify().remove(verify['_id'])
            self.render("%s/verify-reset-finish.html" % _template_path)          
        else:
            self._context.title = u"重置密码"
            fm.render("%s/verify-reset.html" % _template_path, \
                    code=self.get_argument('code', ''), co=self.get_argument('co', ''))
                             
def send_verify_mail(handler, type, to, nickname):
    if type not in ['signup', 'reset']:
        return None
    
    verify = Verify()
    code = verify.hash_code(to)
    verify.create_new(code, type, to)
    
    verify_url = "http://%s/verify-%s?code=%s&co=%s" % (options.domain, type, code, to)
    
    #fr = options.email_from
    #subject = u"[%s]注册确认邮件" % options.sitename
    #body = handler.render_string("mail/sign-up.html", nickname=nickname, verify_url=verify_url)
    #mail.send_email(fr, to, subject, body)    
    
    return verify_url                          

handlers = [
            (r"/sign-in", SigninHandler),
            (r"/sign-out", SignoutHandler),
            (r"/sign-up", SignupHandler),            
            (r"/reset", ResetHandler),
            (r"/verify-signup", VerifySignupHandler), 
            (r"/verify-reset", VerifyResetHandler), 
            ]
