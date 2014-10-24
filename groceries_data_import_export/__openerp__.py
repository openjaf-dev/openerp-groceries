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
    "name": "Groceries Data Import/Export",
    "version": "1.0",
    'author': 'Antonio Mauri Garcia',
    "category": 'Data Load',
    'complexity': "easy",
    "description": """""",
    'website': '',
    'depends': ['base', 'web', 'point_of_sale_gr_ext'],
    'init_xml': [],
    'update_xml': ['view/groceries_import_wizard_view.xml', 'view/base_menu.xml'],
    'js': [
        'static/src/js/import_export_ext.js',
        'static/src/js/main.js'
    ],
    'qweb': [],
    'demo_xml': [],
    'active': False,
    'installable': True,
    'auto_install': True,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
