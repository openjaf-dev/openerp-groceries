# -*- coding: utf-8 -*-

from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp.addons.auth_signup.res_users import SignupError
from openerp.addons.auth_signup.controllers.main import AuthSignupHome as Pepe 



class website_product(http.Controller):

# Product CRUD

    #TODO i have to do the delete product
    @http.route(['/products'], type='http', auth="public", website=True, multilang=True)
    def products(self, **post):
        product_obj = request.registry['product.product']
        product_ids = product_obj.search(request.cr, request.uid, [],
                                     context=request.context)
        values = {
            'product_ids': product_obj.browse(request.cr, request.uid, product_ids,
                                          request.context)
        }
        return request.website.render("website_product.product_index", values)

    @http.route(['/product/<model("product.template"):product>'], type='http', auth="public", website=True, multilang=True)
    def product(self, product, search='', category='', filters='', **kwargs):
        if category:
            category_obj = request.registry.get('product.public.category')
            category = category_obj.browse(request.cr, request.uid, int(category), context=request.context)

        values = {
            'main_object': product,
            'product': product,
            'category': category,
        }
        return request.website.render("website_product.product_show", values)

    @http.route(['/product/<model("product.template"):product>/delete'], type='http', auth="public", website=True, multilang=True)
    def delete(self, product, search='', category='', filters='', **kwargs):
        if product:
            product_obj = request.registry.get('product.template')
            product_ids = [product.id]
#             product_ids += product.id
#             product = product_obj.browse(request.cr, request.uid, int(product), context=request.context)
            product_obj.unlink(request.cr, request.uid, product_ids, context=request.context)
        return request.redirect("/products")


    @http.route(['/create'], type='http', auth="public", website=True, multilang=True)
    def create_a_product(self, **post):
        product = request.registry.get('product.product')
        product.create(request.cr, request.uid, {'name':request.params['name'], 
                                                 'lst_price':float(request.params['price'])})
        return request.redirect("/products")

    @http.route(['/add_product'], type='http', auth="public", website=True, multilang=True)
    def add_product(self, **post):
        values = {
        }
        return request.website.render("website_product.product_new", values)
                
            
# Users CRUD

    #TODO i have to do the delete user....
    #User image not ready....
    @http.route(['/users'], type='http', auth="public", website=True, multilang=True)
    def users(self, **post):
        respartner_obj = request.registry['res.users']
        respartner_ids = respartner_obj.search(request.cr, request.uid, [],
                                     context=request.context)
        values = {
            'respartner_ids': respartner_obj.browse(request.cr, request.uid, respartner_ids,
                                          request.context)
        }
        return request.website.render("website_product.partner_index", values)

    @http.route(['/user/<model("res.partner"):user>'], type='http', auth="public", website=True, multilang=True)
    def user(self, user, search='', filters='', **kwargs):
        if user:
            user_obj = request.registry.get('res.partner')
            user = user_obj.browse(request.cr, request.uid, int(user), context=request.context)

        values = {
            'user': user
        }
        return request.website.render("website_product.user_show", values)

# Session Start

    @http.route(['/pos/session'], type='http', auth="public", website=True, multilang=True)
    def pos_session(self, **post):
    
        values = { }

        pos_session_obj = request.registry['pos.session']
        pos_session_ids = pos_session_obj.search(request.cr, request.uid, ['&',('user_id','=',request.uid), ('state','=','opened')],
                                     context=request.context)
        if not pos_session_ids:                                    
                pos_session_opening_obj = request.registry['pos.session.opening']
                pso_id = pos_session_opening_obj.create(request.cr, request.uid, {}, request.context)
                pos_session_opening_obj.open_session_cb(request.cr, request.uid, [pso_id], request.context)
        
        return request.website.render("website_product.pos_session", values)
        

class AuthSignupHome(Pepe):
    
    @http.route()
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                return super(AuthSignupHome, self).web_login(*args, **kw)
            except (SignupError, AssertionError), e:
                qcontext['error'] = _(e.message)
        
        resgroups_obj = request.registry.get('res.groups')
        groups_ids = resgroups_obj.search(request.cr, request.uid, [], context=request.context)            
        qcontext['groups'] = groups_ids         

        return request.render('auth_signup.signup', qcontext)        
        
        
        
