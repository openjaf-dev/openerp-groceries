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
    'name': 'Point of Sale Groceries Extension',
    'version': '1.0',
    'author': 'Antonio Mauri Garcia',
    'category': 'Point Of Sale',
    'description': "Adding new feature to create a note partner in pos box.",
    'author': 'Groceries S.A',
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_customer.xml',
    ],
    'installable': True,
    'application': True,
    'js': [
        '../web/static/lib/bootstrap/js/bootstrap.js',
        'static/src/lib/bootstrap-typeahead.js',
        'static/src/js/widget_keyboard.js',
        'static/src/js/widgets.js',
        'static/src/js/screens.js',
        'static/src/js/main.js'
    ],
    'css': [
        'static/src/css/pos_ext.css',
        'static/src/css/keyboard_ext.css'
    ],
    'qweb': ['static/src/xml/pos_extended.xml'],
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
