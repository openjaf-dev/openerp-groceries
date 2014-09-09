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
