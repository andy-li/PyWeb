# -*- coding: utf-8 -*-

import logging
from formencode import validators

from pagemanage.src.forms.base import BaseForm
from pagemanage.src.model.products import Product

class ProductForm(BaseForm):
    
    name = validators.String(not_empty=True,max=128, strip=True, messages={'empty':u'请输入产品名称'})
    
    code = validators.String(not_empty=True,max=20, strip=True, messages={'empty':u'请输入产品货号'})
    
    saleprice = validators.Number(not_empty=True, strip=True, messages={'empty':u'请输入产品售价'})
    marketprice = validators.Number(not_empty=True, strip=True, messages={'empty':u'请输入产品原价'})
    url = validators.URL(not_empty=True, max=200, strip=True, messages={'empty':u'请输入产品网址'})
           
    keywords = validators.String(not_empty=True, max=256, strip=True, messages={'empty':u'请输入产品关键字'})
    
    _id = validators.String(not_empty=False)
    
    tips = validators.String(not_empty=False)
    description = validators.String(not_empty=False)

    begindate = validators.String(not_empty=False)
    expdate = validators.String(not_empty=False)
        
    def __after__(self):
        try:
            _id = self._values['_id']    
            code = self._values['code']
            
            keyword = self._values['keywords']
            keyword = keyword.replace('，', ',') 
            keyword = keyword.replace('、', ',')   
                     
            keyword = keyword.split(',')
            keywords = []
            for k in keyword:
                keywords.append(k.strip())
                
            price = {}
            context = {}
            status = {}
                        
            price['sp'] = float(self._values['saleprice']) #售价
            price['mp'] = float(self._values['marketprice']) #市价(原价)
            
            context['keywords'] = keywords
            context['description'] = self._values.get('description', '')
            context['tips'] = self._values.get('tips', '')
            
            status['online'] = 0                               
            status['begindate'] = self._values.get('begindate', '')
            status['expdate'] = self._values.get('expdate', '')
                        
            p = Product()
            p.code = code
            p.name = self._values['name']
            p.url = self._values['url']
                
            p.price = price
            p.context = context
            p.status = status
            
            if not _id:
                if p.findby_code(code):
                    self.add_error('code', u"产品货号已被使用。")
                else:                
                    p.insert()
            else:
                p.updateby_code(code)
                
        except Exception, e:
            logging.error(str(e))
            self.add_error("name", u"保存产品失败，请重试。")  