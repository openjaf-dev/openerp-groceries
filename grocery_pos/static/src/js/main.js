
openerp.point_of_sale_gr_ext = function(instance) {

    instance.point_of_sale_gr_ext = {};

    var module = instance.point_of_sale_gr_ext;

    openerp_pos_keyboard_ext(instance,module);    // import  pos_keyboard_widget_ext.js

    openerp_pos_screens_ext(instance,module);    // import pos_screens_ext.js

    openerp_pos_widgets_ext(instance,module);    // import pos_widgets_ext.js
};

    
