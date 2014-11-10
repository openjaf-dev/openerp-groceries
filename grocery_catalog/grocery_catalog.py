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
import urllib
import Image
from openerp.osv.orm import Model
from tempfile import NamedTemporaryFile

'''
Created on 23/10/2014
@author: José Andrés Hernández Bustio
'''

class grocery_catalog(Model):
    _name = "grocery.catalog"
    _columns = {
        'product_file': fields.binary('Reference Catalog', filename="module_filename", filters='*.xlsx',required=True),
    }

    def import_data(self, cr, uid, ids, context= None):
        obj = self.browse(cr, uid, ids[0])

        if obj.product_file:
            products = self.read_worbook(cr, uid,obj.product_file)
            self.process_data(cr, uid,products)
            obj = self.browse(cr, uid, ids[0])  
                                 
    def read_worbook(self,cr, uid, binary_file, context= None):
        str_file = base64.decodestring(binary_file)
        workbook = xlrd.open_workbook(file_contents=str_file, encoding_override='cp1252')
        products = {}
        for sheet_index in range(workbook.nsheets):
            current_sheet = workbook.sheet_by_index(sheet_index)
            if (current_sheet.name!='media'):
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
            else:
                for row_index in range(1,current_sheet.nrows):
                    upc = current_sheet.cell_value(row_index,1)
                    images = {}
                    for col_index in range(current_sheet.ncols):
                        attribute = current_sheet.cell_value(0,col_index)
                        if attribute.find("Description")>= 0: 
                            attribute = current_sheet.cell_value(row_index,col_index)
                            value = current_sheet.cell_value(row_index,col_index+1)
                            if attribute!='' and value!='':
                                images.update({attribute:value})
                    if upc in products:
                        if 'Images' not in products[upc]:
                            product_values = {'Images':{}}
                            products[upc].update(product_values)
                        products[upc]['Images'].update(images)
        return products
    
    def create_attribute_line(self,cr,uid,value,product_id,context=None):  
        attribute_line_ids = []
        product = self.pool.get('product.product')
        product_attr_line = self.pool.get('product.attribute.line')
        product_attr_value = self.pool.get('product.attribute.value')
        
        product_tmpl_id = -1
        if product_id:
            product_tmpl_id = product.browse(cr, uid, product_id, context=context).product_tmpl_id.id
    
            
        for attr_value_id in value:
            attr_value = product_attr_value.browse(cr, uid, attr_value_id, context=context)
            attr_id = attr_value.attribute_id.id
            p_attr_line = -1
            if product_tmpl_id !=-1:
                p_attr_line = product_attr_line.search(cr, uid, [('product_tmpl_id', '=', product_tmpl_id),('attribute_id', '=', attr_id)], context=context)
            if p_attr_line !=-1:
                attr_line = [1,p_attr_line[0]]
            else:
                attr_line = [0,False]
            attr_value_ids = []
            attr_line_value = {}

            attr_line_value['attribute_id'] = attr_id
            attr_value_ids.append(attr_value.id)
            attr_line_value['value_ids'] =[[6,False,attr_value_ids]]
            attr_line.append(attr_line_value)
            attribute_line_ids.append(attr_line)
        return attribute_line_ids
            
            
        
    def create_attribute_value(self,cr,uid,value,context=None):
        CAMPOS = {'UPC','GS1 Category','Item Description','Marketing Description','Images'}
        attr_value_ids = []
        attr = self.pool.get('product.attribute')
        attr_value = self.pool.get('product.attribute.value')
        for k,v in value.items():
            if v != '':
                if k not in CAMPOS:
                    at_ids = attr.search(cr, uid, [('name', '=', k)], context=context)
                    if not at_ids:
                        vals = {'name': k}
                        attr_id = attr.create(cr, uid, vals, context)
                    else:
                        attr_id = at_ids[0]
                        
                    at_value_ids = attr_value.search(cr, uid, [('name', '=', v),('attribute_id', '=', attr_id)], context=context)
                    if not at_value_ids:
                        vals = {'name': v, 'attribute_id': attr_id}
                        attr_value_id = attr_value.create(cr, uid, vals, context)
                    else:
                        attr_value_id = at_value_ids[0]
                    
                    attr_value_ids.append(attr_value_id)       
        return attr_value_ids
                
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

    def get_image(self,cr,uid,images,context=None):
        proxies = {'http': 'http://jose.hernandez%40icrt.cu:Jose@ndres272427@10.3.2.12:3128'}
        for k,v in images.items():
            url = v
            if k.find("Front")>= 0:
                online_image = urllib.urlopen(url,proxies=proxies)
                EXJPG = ".jpg"
                other_format = NamedTemporaryFile()
                jpg_format = NamedTemporaryFile(suffix=EXJPG)
                other_format.write(online_image.read())
                other_format.flush()
                Image.open(other_format.name).save(jpg_format.name)
                image_file = tools.file_open(jpg_format.name, 'rb')
                file_data = image_file.read()  
        return base64.encodestring(file_data)
    
    def process_data(self,cr, uid, products,context=None):
        
        product = self.pool.get('product.product')
        
        for k, product_data in products.items():
            category_id = self.create_category(cr,uid,product_data['GS1 Category'])
            name = product_data['Item Description']
            description = product_data['Marketing Description']
            default_code = product_data['UPC']
            if 'Images' in product_data:
                image = self.get_image(cr,uid,product_data['Images'],context)
            attribute_value_ids = self.create_attribute_value(cr, uid, product_data, context)
            
            product_id = product.search(cr, uid, [('default_code', '=', default_code)], context=context)
            attribute_line_ids = self.create_attribute_line(cr,uid,attribute_value_ids,product_id,context) 
            
            vals = {'name': name,
                    'categ_id' : category_id,
                    'description' : description,
                    'default_code' : default_code,
                    'attribute_line_ids':attribute_line_ids,
                    'image':image,
                    }
            if product_id:
                product.write(cr,uid,product_id,vals,context)  
            else:
               product_id = product.create(cr,uid,vals,context)
