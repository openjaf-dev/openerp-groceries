# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
from PIL import Image

from openerp import tools
from openerp.osv import fields, osv
from openerp.osv.orm import Model
from openerp.tools.translate import _

class pos_customer(Model):
    _inherit = 'res.partner'
    _order = 'id desc'

    def _get_last_note(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for obj in self.browse(cr, uid, ids, context):
            res[obj.id] = False
            if obj.notes:
                res[obj.id] = obj.notes[-1].comment
        return res

    def create_from_ui(self, cr, uid, customer, context=None):
        pn = self.pool.get('pos.note')

        customer_id = customer.get('id', False)
        if not customer_id:
            vals = {
                'name': customer['name'],
                'mobile': customer.get('phone', False),
                'email': customer.get('email', False)
            }
            customer_id = self.create(cr, uid, vals, context)

        if customer.get('note', False):
            wals = {'comment': customer['note'], 'pos_customer': customer_id}
            pn.create(cr, uid, wals, context)

        return customer_id

    _columns = {
        'notes': fields.one2many('pos.note', 'pos_customer', 'Notes'),
        'last_note': fields.function(_get_last_note, method=True, type='char',
                                     size='255', string='Last Note'),
        'name': fields.char(string='Name', size=128, required=True,
                            select=True),
    }


class pos_customer_comments(Model):
    _name = 'pos.note'
    _order = 'id asc'
    _columns = {
        'pos_customer': fields.many2one('res.partner', 'Customer Note',
                                        required=True, ondelete='cascade'),
        'comment': fields.text('Notes'),
    }

class pos_credit_cards_conf(Model):
    _name = 'pos.credit.cards.conf'
    _inherit = ['mail.thread']

    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image, avoid_resize_medium=True)
        return result

    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)

    _columns = {
        'name': fields.char(string='Name', size=128, required=True, translate=True, select=True),
        'image': fields.binary("Image",
                           help="This field holds the image used as image for the product, limited to 1024x1024px."),
        'image_medium': fields.function(_get_image, fnct_inv=_set_image,string="Medium-sized image", type="binary",
                multi="_get_image", help="Medium-sized image of the product. It is automatically "
                 "resized as a 128x128px image, with aspect ratio preserved, "
                 "only when the image exceeds one of those sizes. Use this field in form views or some kanban views."),
        'image_small': fields.function(_get_image, fnct_inv=_set_image,string="Small-sized image", type="binary",
               multi="_get_image",help="Small-sized image of the product. It is automatically "
               "resized as a 64x64px image, with aspect ratio preserved. "
               "Use this field anywhere a small image is required."),
        'ready_2_use': fields.boolean('To Use', help="Specify if the credit card can be used."),
    }

    def _check_image_size(self, cr, uid, ids, context=None):
        obj_self = self.browse(cr, uid, ids[0], context=context)

        image_stream = StringIO.StringIO(obj_self.image.decode('base64'))
        image = Image.open(image_stream)
        perm_size = (32, 32)
        if not perm_size == image.size:
            return False
        else:
            return True

    _constraints = [
        (_check_image_size, '\nThe card image must have a size of 32 x 32!', ['image']),
    ]

class account_journal(osv.osv):
    _inherit = "account.journal"

    def _get_credit_cards_json(self, cr, uid, ids, field_name, arg=None, context=None):
        res = dict.fromkeys(ids, '')
        for journal in self.browse(cr, uid, ids, context=context):
            credit_cards = journal.credit_cards
            if credit_cards:
                for c_card in credit_cards:
                    res[journal.id] = res[journal.id] + str(c_card.id) + ':' + c_card.name + ','
        return res

    _columns = {
        'credit_cards': fields.many2many('pos.credit.cards.conf', 'pos_credit_cards_conf_journal_rel',
        'journal_id', 'pos_credit_cards_conf_id', 'Available Credit Cards', domain="[('ready_2_use', '=', True )]"),
        'credit_cards_json_str': fields.function(_get_credit_cards_json, string='Card Json Encoding', type='char',
                                                 size=10000000),
    }


class pos_order_gr_ext(Model):
    _inherit = 'pos.order'

    def create_from_ui(self, cr, uid, orders, context=None):
        order_ids = []
        order_id = None

        for tmp_order in orders:
            to_invoice = tmp_order['to_invoice']
            order = tmp_order['data']

            if not self.search(cr, uid, [('pos_reference', '=', order['name'])]):
                order_id = self.create(cr, uid, {
                    'name': order['name'],
                    'user_id': order['user_id'] or False,
                    'session_id': order['pos_session_id'],
                    'lines': order['lines'],
                    'pos_reference': order['name'],
                    'partner_id': order['partner_id'] or False
                }, context)
            for payments in order['statement_ids']:
                payment = payments[2]
                self.add_payment(cr, uid, order_id, {
                    'amount': payment['amount'] or 0.0,
                    'payment_date': payment['name'],
                    'statement_id': payment['statement_id'],
                    'payment_name': payment.get('note', False),
                    'journal': payment['journal_id']
                }, context=context)

            if order['amount_return']:
                session = self.pool.get('pos.session').browse(cr, uid, order['pos_session_id'], context=context)
                cash_journal = session.cash_journal_id
                if not cash_journal:
                    cash_journal_ids = filter(lambda st: st.journal_id.type=='cash', session.statement_ids)
                    if not len(cash_journal_ids):
                        raise osv.except_osv( _('error!'),
                            _("No cash statement found for this session. Unable to record returned cash."))
                    cash_journal = cash_journal_ids[0].journal_id
                self.add_payment(cr, uid, order_id, {
                    'amount': -order['amount_return'],
                    'payment_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'payment_name': _('return'),
                    'journal': cash_journal.id,
                }, context=context)
            order_ids.append(order_id)
            self.signal_paid(cr, uid, [order_id])

            if to_invoice:
                self.action_invoice(cr, uid, [order_id], context)
                order_obj = self.browse(cr, uid, order_id, context)
                self.pool['account.invoice'].signal_invoice_open(cr, uid, [order_obj.invoice_id.id])

        return order_ids
