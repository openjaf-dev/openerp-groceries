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

from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
import logging
import pdb
import time
from openerp.osv.orm import Model
from openerp.osv.orm import TransientModel
import openerp
from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _

import openerp.addons.decimal_precision as dp
import openerp.addons.product.product

import random

_logger = logging.getLogger(__name__)

class posi_session(Model):
    _name = 'posi.session'
    _order = 'id desc'

    POSI_SESSION_STATE = [
        ('opening_control', 'Opening Control'),  # Signal open
        ('opened', 'In Progress'),                    # Signal closing
        ('closing_control', 'Closing Control'),  # Signal close
        ('closed', 'Closed & Posted'),
    ]

    _columns = {
        'name': fields.char('Session ID', size=32, required=True, readonly=True),
        'user_id': fields.many2one('res.users', 'Responsible',
                                    required=True,
                                    select=1,
                                    readonly=True,
                                    states={'opening_control' : [('readonly', False)]}
                                   ),
        'start_at': fields.datetime('Opening Date', readonly=True),
        'stop_at': fields.datetime('Closing Date', readonly=True),

        'state': fields.selection(POSI_SESSION_STATE, 'Status',
                required=True, readonly=True,
                select=1),
        'sequence_id' : fields.many2one('ir.sequence', 'Order IDs Sequence', readonly=True,
            help="This sequence is automatically created by OpenERP but you can change it "\
                "to customize the reference numbers of your orders."),
    }

    _defaults = {
        'name': '/',
        'user_id': lambda obj, cr, uid, context: uid,
        'state': 'opening_control',
    }

    _sql_constraints = [
        ('uniq_name', 'unique(name)', "The name of this POSI Session must be unique !"),
    ]

    def add_product_qty_from_ui(self, cr, uid, data, context=None):
        stock_change_product_qty_obj = self.pool.get('stock.change.product.qty')
        stock_change_product_qty_id = stock_change_product_qty_obj.create(cr, uid, data)
        stock_change_product_qty_obj.change_product_qty(cr, uid, [stock_change_product_qty_id], context)
        return True

    def _check_unicity(self, cr, uid, ids, context=None):
        for session in self.browse(cr, uid, ids, context=None):
            # open if there is no session in 'opening_control', 'opened', 'closing_control' for one user
            domain = [
                ('state', 'not in', ('closed', 'closing_control')),
                ('user_id', '=', session.user_id.id)
            ]
            count = self.search_count(cr, uid, domain, context=context)
            if count > 1:
                return False
        return True

    _constraints = [
        (_check_unicity, "You cannot create two active sessions with the same responsible!", ['user_id', 'state']),
    ]

    def create(self, cr, uid, values, context=None):
        context = context or {}

        values.update({
            'name': str(random.random()),
        })

        return super(posi_session, self).create(cr, uid, values, context=context)

    def open_cb(self, cr, uid, ids, context=None):
        """
        call the Point Of Stock Inventory interface and set the posi.session to 'opened' (in progress)
        """
        if context is None:
            context = dict()

        if isinstance(ids, (int, long)):
            ids = [ids]

        this_record = self.browse(cr, uid, ids[0], context=context)
        this_record.signal_workflow('open')

        context.update(active_id=this_record.id)

        return {
            'type': 'ir.actions.act_url',
            'url' : '/posi/web/',
            'target': 'self',
        }

    def wkf_action_open(self, cr, uid, ids, context=None):
        # second browse because we need to refetch the data from the DB for cash_register_id
        for record in self.browse(cr, uid, ids, context=context):
            values = {}
            if not record.start_at:
                values['start_at'] = time.strftime('%Y-%m-%d %H:%M:%S')
            values['state'] = 'opened'
            record.write(values, context=context)

        return self.open_frontend_cb(cr, uid, ids, context=context)

    def wkf_action_opening_control(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'opening_control'}, context=context)

    def wkf_action_closing_control(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'closing_control', 'stop_at': time.strftime('%Y-%m-%d %H:%M:%S')},
                          context=context)

    def wkf_action_close(self, cr, uid, ids, context=None):
        # Close CashBox
        self.write(cr, uid, ids, {'state': 'closed'}, context=context)

        obj = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'point_of_stock_inventory',
                                                                  'menu_point_stock_inventory_root')[1]
        return {
            'type': 'ir.actions.client',
            'name': 'Point of Stock Inventory Menu',
            'tag': 'reload',
            'params': {'menu_id': obj},
        }

    def open_frontend_cb(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        if not ids:
            return {}
        for session in self.browse(cr, uid, ids, context=context):
            if session.user_id.id != uid:
                raise osv.except_osv(
                        _('Error!'),
                        _("You cannot use the session of another users. This session is owned by %s. Please first "
                          "close this one to use this point of sale." % session.user_id.name))
        context.update({'active_id': ids[0]})
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url':   '/posi/web/',
        }

import io
import StringIO

class ean_wizard(TransientModel):
    _name = 'posi.ean_wizard'
    _columns = {
        'ean13_pattern': fields.char('Reference', size=32, required=True, translate=True),
    }
    def sanitize_ean13(self, cr, uid, ids, context):
        for r in self.browse(cr, uid, ids):
            ean13 = openerp.addons.product.product.sanitize_ean13(r.ean13_pattern)
            m = context.get('active_model')
            m_id = context.get('active_id')
            self.pool[m].write(cr, uid, [m_id], {'ean13':ean13})
        return {'type': 'ir.actions.act_window_close'}

import simplejson

class product_product(Model):
    _inherit = 'product.product'

    def _quantity_alert(self, cr, uid, ids, name, args, context=None):
        res = {}
        investors = []

        if context is None:
            context = {}

        for product in self.browse(cr, uid, ids):
            if product.qty_available > 0:
                res[product.id] = False
            else:
                res[product.id] = True
        return res

    def _get_procurements_json(self, cr, uid, ids, field_name, arg=None, context=None):
        res = dict.fromkeys(ids, '')
        for product in self.browse(cr, uid, ids, context=context):
            procurement_orders = product.procurement_order_ids
            if procurement_orders:
                proc_dicc = {}
                for procurement_order in procurement_orders:
                    description = procurement_order.message or procurement_order.state
                    proc_dicc.update({procurement_order.id: {'state':procurement_order.state,
                                                             'description': description}})
                res[product.id] = simplejson.dumps(proc_dicc)
        return res

    _columns = {
        'available_in_posi': fields.boolean('Available in the Point of Stock Inventory',
                                    help='Check if you want this product to appear in the Point of Stock Inventory'),
        'qty_alert': fields.function(_quantity_alert, type='boolean', string='Quantity Alert'),
        'procurements_json_str': fields.function(_get_procurements_json, string='Order Procurements JSON', type='char',
                                                 size=10000000),
        'procurement_order_ids': fields.one2many('procurement.order', 'product_id', 'Order Procurements'),
    }

    _defaults = {
        'available_in_posi': True,
    }

    def edit_ean(self, cr, uid, ids, context):
        return {
            'name': _("Assign a Custom EAN"),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'posi.ean_wizard',
            'target': 'new',
            'view_id': False,
            'context': context,
        }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
