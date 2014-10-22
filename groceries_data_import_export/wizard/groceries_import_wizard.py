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

'''
Created on 26/3/2014
@author: Victor Gonzalez Gonzalez
'''

class groceries_import_wizard(osv.osv_memory):

    def _get_image(self, cr, uid, context=None):
        path = os.path.join('groceries_data_import_export','res','config_pixmaps','%d.png'%random.randrange(1,4))
        image_file = file_data = tools.file_open(path,'rb')
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
        'product_category_file': fields.binary('Product Category File',
                                     filename="module_filename",
                                     help="Account Type File.\n"
                                     "File Format: code*name*report_type*"
                                     "close_method \n"
                                     "Example: actv*ACTIVOS/Vista*none*none",
                                     filters='*.xls'),
        'config_logo': fields.function(_get_image_fn, string='Image', type='binary', readonly=True),
    }

    _defaults = {
        'config_logo': _get_image
    }

    def check_product_category_step1(self, cr, uid, ids, context=None):
        #objetos necesarios para el parseador
        obj = self.browse(cr, uid, ids[0])

        if obj.product_category_file:
            product_category_file_obj = obj.product_category_file
            str_file = base64.decodestring(product_category_file_obj)
            workbook = xlrd.open_workbook(file_contents=str_file, encoding_override='cp1252')
            # worksheet = self.workbook.sheet_by_index(0)
            # num_rows = self.worksheet.nrows - 1
            # num_cells = self.worksheet.ncols - 1



            return False

    def check_format_account_type(self, element, len_format):
        """
        Metodo que valida que la linea del tipo de cuenta contenga la
        cantidad de elementos del formato
        """
        item_element = element.split('*')
        if len(item_element) == len_format:
            return True
        return False

groceries_import_wizard()
