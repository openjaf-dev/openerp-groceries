# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010, 2014 Tiny SPRL (<http://tiny.be>).
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

import requests

from openerp.osv.orm import TransientModel


class cenit_client(TransientModel):
    _name = 'cenit.client'

    def notify(self, cr, uid, obj, context=None):
        model = self.pool.get(obj._name)
        payload = model.serialize(obj, context)

        # TODO: el add_product se debe construir dinamicamente
        url = 'http://localhost:3000/cenit/add_product'
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=payload, headers=headers)
        return r.status_code
