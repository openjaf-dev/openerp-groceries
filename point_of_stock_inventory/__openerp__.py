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


{
    'name': 'Point of Stock Inventory',
    'version': '1.0.1',
    'category': 'Point Of Stock Inventory',
    'sequence': 6,
    'summary': 'Touchscreen Interface for Shops',
    'description': """
Quick and Easy Inventory process
===========================

This module allows you to manage your shop stock very easily with a fully web based touchscreen interface.
It is compatible with all PC tablets and the iPad.

Add Products can be done in several ways:

* Using a barcode reader
* Browsing through categories of products or via a text search.

Main Features
-------------
***
    """,
    'author': 'Antonio Mauri Garcia',
    'images': ['images/pos_touch_screen.jpeg', 'images/pos_session.jpeg', 'images/pos_analysis.jpeg','images/sale_order_pos.jpeg','images/product_pos.jpeg'],
    'depends': ['point_of_sale_gr_ext'],
    'data': [
        'views/point_of_stock_inventory_view.xml',
    ],
    'demo': [

    ],
    'test': [

    ],
    'installable': True,
    'application': True,
    'js': [
        'static/lib/fastclick.js',
        'static/src/js/db.js',
        'static/src/js/models.js',
        'static/src/js/widget_base.js',
        'static/src/js/widget_keyboard.js',
        'static/src/js/widgets.js',
        'static/src/js/devices.js',
        'static/src/js/screens.js',
        'static/src/js/main.js',
    ],
    'qweb': ['static/src/xml/posi.xml'],
    'auto_install': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
