# -*- coding: utf-8 -*-

from openerp.addons.web import http
from openerp.addons.web.http import request


class website_product(http.Controller):

# Product CRUD

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
#             'main_object': product,
            'user': user
        }
        return request.website.render("website_product.user_show", values)

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
        
    
    
        
        
