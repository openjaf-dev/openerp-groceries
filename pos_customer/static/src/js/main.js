
openerp.pos_customer = function(instance) {

    instance.pos_customer = {};

    var module = instance.pos_customer;

    openerp_pos_keyboard_ext(instance, module);    // import  pos_keyboard_widget.js

    openerp_pos_screens_ext(instance, module);    // import pos_screens_ext.js

    openerp_pos_widgets_ext(instance, module);    // import pos_widgets_ext.js
};

    
