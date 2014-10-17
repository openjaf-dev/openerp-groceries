function openerp_pos_widgets_ext(instance, module){ //module is instance.point_of_sale_gr_ext
    var QWeb = instance.web.qweb;
    var _t = instance.web._t;

    // The PosWidget is the main widget that contains all other widgets in the PointOfSale.
    // It is mainly composed of :
    // - a header, containing the list of orders
    // - a leftpane, containing the list of bought products (orderlines)
    // - a rightpane, containing the screens (see pos_screens.js)
    // - an actionbar on the bottom, containing various action buttons
    // - popups
    // - an onscreen keyboard
    // a screen_selector which controls the switching between screens and the showing/closing of popups

    module.PosGrWidget = instance.point_of_sale.PosWidget.include({


    });
}
