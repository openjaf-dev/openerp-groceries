
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.osv.orm import TransientModel
from openerp.addons.point_of_stock_inventory.point_of_stock_inventory import posi_session


class posi_session_opening(TransientModel):
    _name = 'posi.session.opening'

    _columns = {
        'posi_session_id': fields.many2one('posi.session', 'PoSi Session'),
        'posi_state': fields.related('posi_session_id', 'state',
                                     type='selection',
                                     selection=posi_session.POSI_SESSION_STATE,
                                     string='Session Status', readonly=True),
        'posi_state_str': fields.char('Status', 32, readonly=True),
        'posi_session_name': fields.related('posi_session_id', 'name',
                                            type='char', size=64, readonly=True),
        'posi_session_username': fields.related('posi_session_id', 'user_id', 'name',
                                                type='char', size=64, readonly=True)
    }

    def open_ui(self, cr, uid, ids, context=None):
        context = context or {}
        data = self.browse(cr, uid, ids[0], context=context)
        context['active_id'] = data.posi_session_id.id
        return {
            'type' : 'ir.actions.act_url',
            'url':   '/posi/web/',
            'target': 'self',
        }

    def open_existing_session_cb_close(self, cr, uid, ids, context=None):
        return self.open_session_cb(cr, uid, ids, context)

    def open_session_cb(self, cr, uid, ids, context=None):
        assert len(ids) == 1, "you can open only one session at a time"
        proxy = self.pool.get('posi.session')
        wizard = self.browse(cr, uid, ids[0], context=context)
        if not wizard.posi_session_id:
            values = {
                'user_id' : uid,
            }
            session_id = proxy.create(cr, uid, values, context=context)
            s = proxy.browse(cr, uid, session_id, context=context)
            return self.open_ui(cr, uid, ids, context=context)
            # return self._open_session(session_id)
        return self._open_session(wizard.posi_session_id.id)

    def open_existing_session_cb(self, cr, uid, ids, context=None):
        assert len(ids) == 1
        wizard = self.browse(cr, uid, ids[0], context=context)
        return self._open_session(wizard.posi_session_id.id)

    def _open_session(self, session_id):
        return {
            'name': _('Session'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'posi.session',
            'res_id': session_id,
            'view_id': False,
            'type': 'ir.actions.act_window',
        }

    def on_change_config(self, cr, uid, ids, config_id, context=None):
        result = {
            'posi_session_id': False,
            'posi_state': False,
            'posi_state_str': '',
            'posi_session_username': False,
            'posi_session_name': False,
        }
        if not config_id:
            return {'value': result}
        proxy = self.pool.get('posi.session')
        session_ids = proxy.search(cr, uid, [
            ('state', '!=', 'closed'),
            ('user_id', '=', uid),
        ], context=context)
        if session_ids:
            session = proxy.browse(cr, uid, session_ids[0], context=context)
            result['posi_state'] = str(session.state)
            result['posi_state_str'] = dict(posi_session.POSI_SESSION_STATE).get(session.state, '')
            result['posi_session_id'] = session.id
            result['posi_session_name'] = session.name
            result['posi_session_username'] = session.user_id.name

        return {'value': result}