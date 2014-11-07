# -*- coding: utf-8 -*-

from openerp.osv import osv, fields


class product(osv.osv):
    _inherit = 'product.product'
    _columns = {
        'website_published': fields.boolean('Available in the website')        
    }
    _defaults = {
        'website_published': False
    }

    def img(self, cr, uid, ids, field='image_small', context=None):
        return "/website/image?model=%s&field=%s&id=%s" % (self._name, field, ids[0])
