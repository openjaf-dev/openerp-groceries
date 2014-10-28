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

import os
import random

from openerp.osv import fields, osv
from openerp.tools.translate import _
import base64
import openerp.tools as tools
import xlrd
from openerp.osv.orm import TransientModel

'''
Created on 23/10/2014
@author: Antonio Mauri Garcia
'''

class groceries_import_wizard(TransientModel):

    def _get_image(self, cr, uid, context=None):
        path = os.path.join('groceries_data_import_export', 'res', 'config_pixmaps', '%d.png' % random.randrange(1, 4))
        image_file = tools.file_open(path, 'rb')
        try:
            file_data = image_file.read()
            return base64.encodestring(file_data)
        finally:
            image_file.close()

    def _get_image_fn(self, cr, uid, ids, name, args, context=None):
        image = self._get_image(cr, uid, context)
        return dict.fromkeys(ids, image)

    _name = "groceries.import.wizard"
    _columns = {
        'product_category_file': fields.binary('Reference Catalogue', filename="module_filename", filters='*.xlsx',
                                               required=True),
        'config_logo': fields.function(_get_image_fn, string='Image', type='binary', readonly=True),
    }

    _defaults = {
        'config_logo': _get_image
    }

    def check_product_category_step1(self, cr, uid, ids, context= None):
        obj = self.browse(cr, uid, ids[0])

        if obj.product_category_file:
            products = self.read_worbook(cr, uid,obj.product_category_file)
            self.process_data(cr, uid,products)
            obj = self.browse(cr, uid, ids[0])
            return {
                 'view_type': 'form',
                 'name': 'Finish',
                 'view_mode': 'form',
                 'res_model': 'groceries.import.wizard1',
                 'views': [],
                 'type': 'ir.actions.act_window',
                 'target': 'new',
                 'context': {
                 }
            }   
                    
    def read_worbook(self,cr, uid, binary_file, context= None):
        str_file = base64.decodestring(binary_file)
        workbook = xlrd.open_workbook(file_contents=str_file, encoding_override='cp1252')
        products = {}
        for sheet_index in range(workbook.nsheets):
            current_sheet = workbook.sheet_by_index(sheet_index)
            for row_index in range(1,current_sheet.nrows):
                upc = current_sheet.cell_value(row_index,1)
                product_values = {}
                for col_index in range(current_sheet.ncols):
                    attribute = current_sheet.cell_value(0,col_index)
                    value = current_sheet.cell_value(row_index,col_index)
                    product_values.update({attribute:value})    
                if upc in products:
                    products[upc].update(product_values)
                else:
                    if sheet_index == 1: 
                        product = {upc:{}}
                        products.update(product)                
                        products[upc].update(product_values)
        return products

    def create_category(self, cr, uid,value,context=None): 
        if not value:
            return False
        if value.rindex('(') > 0:
            value = value[value.index(')')+2:value.rindex('(')-1]
        else:
            value = value[value.index(')')+2:]
        category_tree = value.split('/')
        pc = self.pool.get('product.category')
        current_catg = False
        for category in category_tree:
            categ_id = pc.search(cr, uid, [('name', '=', category)], context=context)
            if categ_id:
                current_catg = categ_id[0]
            else:
                vals = {'name': category, 'parent_id': current_catg}
                current_catg = pc.create(cr, uid, vals, context)
        return current_catg

    def process_data(self,cr, uid, products,context=None):
        for k, product_data in products.items():
            category_id = self.create_category(cr,uid,product_data['GS1 Category'])
            name = product_data['Item Description']
            description = product_data['Marketing Description']
            default_code = product_data['UPC']
            
            product = self.pool.get('product.product')
            product_id = product.search(cr, uid, [('default_code', '=', default_code)], context=context)
            vals = {'name': name,
                    'categ_id':category_id,
                    'description':description,
                    'default_code':default_code,
                    }
            if product_id:
                product.write(cr,uid,product_id,vals,context)
            else:
                product.create(cr,uid,vals,context)
        
groceries_import_wizard()

class groceries_import_wizard_1(TransientModel):

    def _get_image(self, cr, uid, context=None):
        path = os.path.join('groceries_data_import_export', 'res', 'config_pixmaps', '%d.png' % random.randrange(1, 4))
        image_file = tools.file_open(path, 'rb')
        try:
            file_data = image_file.read()
            return base64.encodestring(file_data)
        finally:
            image_file.close()

    def _get_image_fn(self, cr, uid, ids, name, args, context=None):
        image = self._get_image(cr, uid, context)
        return dict.fromkeys(ids, image)

    _name = "groceries.import.wizard1"
    _columns = {
        'product_file': fields.binary('Product File', filename="module_filename", filters='*.xlsx',
                                               required=True),
        'config_logo': fields.function(_get_image_fn, string='Image', type='binary', readonly=True),
    }

    _defaults = {
        'config_logo': _get_image
    }

    def check_product_step2(self, cr, uid, ids, context= None):
        return False

groceries_import_wizard_1()
