# -*- coding: utf-8 -*-

from openerp.addons.web import http
from openerp.addons.web.http import request

class website_product(http.Controller):

    @http.route(['/products'], type='http', auth="public", website=True, multilang=True)
    def blog(self, **post):
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
