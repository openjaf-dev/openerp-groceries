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
        return request.website.render("website_product.products_crud", values)

