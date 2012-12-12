# -*- coding: utf-8 -*-

from tornado.options import options

from pagemanage.src.libs.handler import AdminBaseHandler
from pagemanage.src.libs.utils import pagevar
from pagemanage.src.forms.product import ProductForm
from pagemanage.src.model.products import Product

_sidebar_links = {
                 'product':u'产品列表',
                 'product/create':u'新增产品',
                 'product/search':u'产品搜索',
                 }

class ProductListHandler(AdminBaseHandler):
    _handler_template = "admin/product.html"
    page = 1
    pagesize = 10
    
    def get(self):        
        args = {}
        args['kw'] = 'france'
        args['online'] = 1
        self.page = pagevar(self.get_argument('page', 1))
        products = self.__get_products()   
        self.render(self._handler_template, data=products, 
                    page=self.page, num=products.count(), pagesize=self.pagesize, 
                    args=args)
            
    def prepare(self):
        super(ProductListHandler, self).prepare()
        self._context.title = u"产品列表"
        self._context.sidebar_links = _sidebar_links
    
    def __get_products(self):
        return Product().get_list(page=self.page, pagesize=self.pagesize)
    
class ProductCreateHandler(AdminBaseHandler):
    _handler_template = "admin/product-create.html"   
    
    def get(self):        
        self.render(self._handler_template, product={})
        
    def post(self):
        fm = ProductForm(self)
        if fm.validate():
            keep = self.get_argument('keep_create', None)
            if keep:
                self.redirect(options.admin_url+'/product/create')
            else:
                self.redirect(options.admin_url+'/product')
        else:
            fm.render(self._handler_template, product={})

    def prepare(self):
        super(ProductCreateHandler, self).prepare()
        self._context.title = u"新增产品"
        self._context.sidebar_links = _sidebar_links       

class ProductRemoveHandler(AdminBaseHandler):
    def get(self):
        code = self.get_argument('code', '')
        if code:
            try:
                #Product().deleteby_code(code)
                self.write('success')
            except Exception:
                self.write('fail')

class ProductEditHandler(AdminBaseHandler):
    _handler_template = "admin/product-edit.html"
    
    def get(self, code):        
        self.render(self._handler_template, product=self.__get_product(code))

    def post(self, code):                
        fm = ProductForm(self)
        if fm.validate():
            self.redirect(options.admin_url+'/product')                        
        else:
            fm.render(self._handler_template, product=self.__get_product(code))

    def prepare(self):
        super(ProductEditHandler, self).prepare()
        self._context.title = u"查看产品"
        self._context.sidebar_links = _sidebar_links
                
    def __get_product(self, code):
        product = Product().findby_code(code)
        product['keywords'] = ','.join(product['context'].get('keywords', []))
        return product

class ProductSearchHandler(AdminBaseHandler):
    _handler_template = "admin/product-search.html"
    
    def get(self):
        self.render(self._handler_template)
        
    def prepare(self):
        super(ProductSearchHandler, self).prepare()
        self._context.sidebar_links = _sidebar_links

handlers = [
            (r"%s/product" % options.admin_url, ProductListHandler),            
            (r"%s/product/create" % options.admin_url, ProductCreateHandler),
            (r"%s/product/remove" % options.admin_url, ProductRemoveHandler),
            (r"%s/product/edit/([A-Z0-9]{8,16})" % options.admin_url, ProductEditHandler),
            (r"%s/product/search" % options.admin_url, ProductSearchHandler),
            ]
