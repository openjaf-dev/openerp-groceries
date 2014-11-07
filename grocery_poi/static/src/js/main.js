
openerp.point_of_stock_inventory = function(instance) {

    instance.point_of_stock_inventory = {};

    var module = instance.point_of_stock_inventory;

    openerp_posi_db(instance,module);         // import db.js

    openerp_posi_models(instance,module);     // import posi_models.js

    openerp_posi_basewidget(instance,module); // import posi_basewidget.js

    openerp_posi_keyboard(instance,module);   // import  posi_keyboard_widget.js

    openerp_posi_screens(instance,module);    // import posi_screens.js

    openerp_posi_devices(instance,module);    // import posi_devices.js
    
    openerp_posi_widgets(instance,module);    // import posi_widgets.js

    instance.web.client_actions.add('posi.ui', 'instance.point_of_stock_inventory.PosWidget');
};

    
