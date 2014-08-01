function openerp_pos_widgets_ext(instance, module){ //module is instance.point_of_sale_gr_ext
    var QWeb = instance.web.qweb;
	var _t = instance.web._t;

    // The NotesWidget is the widget that show the customer note popup in the PointOfSale.

    module.NotesWidget = instance.point_of_sale.PosBaseWidget.extend({
        template: 'NotesWidget',
        init: function(parent, options){
            var options = options || {};
            this.pos = options.pos;
            this._super(parent,options);
            this.mode = options.mode || 'cashier';
        },
        set_user_mode: function(mode){
            this.mode = mode;
            this.refresh();
        },
        refresh: function(){
            this.renderElement();
        },
        renderElement: function(){
            var self = this;
            this._super();

            this.$el.click(function(parent){
                /*self.new_customer_note_popup = new module.NotesPopupWidget(self.pos_widget, {});
                self.new_customer_note_popup.appendTo(self.pos_widget.$el);*/

               /* self.pos_widget.screen_selector.add_popup('customer_note',self.new_customer_note_popup);*/
                self.pos_widget.screen_selector.show_popup('new_customer_note_popup');
            });

        },
        get_name: function(){
            return _t("Notes");
        },
    });

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

        // This method instantiates all the screens, widgets, etc. If you want to add new screens change the
        // startup screen, etc, override this method.
        build_widgets: function() {
            var self = this;

            // --------  Screens ---------

            this.product_screen = new instance.point_of_sale.ProductScreenWidget(this,{});
            this.product_screen.appendTo(this.$('.screens'));

            this.receipt_screen = new instance.point_of_sale.ReceiptScreenWidget(this, {});
            this.receipt_screen.appendTo(this.$('.screens'));

            this.payment_screen = new instance.point_of_sale.PaymentScreenWidget(this, {});
            this.payment_screen.appendTo(this.$('.screens'));

            this.welcome_screen = new instance.point_of_sale.WelcomeScreenWidget(this,{});
            this.welcome_screen.appendTo(this.$('.screens'));

            this.client_payment_screen = new instance.point_of_sale.ClientPaymentScreenWidget(this, {});
            this.client_payment_screen.appendTo(this.$('.screens'));

            this.scale_invite_screen = new instance.point_of_sale.ScaleInviteScreenWidget(this, {});
            this.scale_invite_screen.appendTo(this.$('.screens'));

            this.scale_screen = new instance.point_of_sale.ScaleScreenWidget(this,{});
            this.scale_screen.appendTo(this.$('.screens'));

            // --------  Popups ---------

            this.help_popup = new instance.point_of_sale.HelpPopupWidget(this, {});
            this.help_popup.appendTo(this.$el);

            this.error_popup = new instance.point_of_sale.ErrorPopupWidget(this, {});
            this.error_popup.appendTo(this.$el);

            this.error_product_popup = new instance.point_of_sale.ProductErrorPopupWidget(this, {});
            this.error_product_popup.appendTo(this.$el);

            this.error_session_popup = new instance.point_of_sale.ErrorSessionPopupWidget(this, {});
            this.error_session_popup.appendTo(this.$el);

            this.choose_receipt_popup = new instance.point_of_sale.ChooseReceiptPopupWidget(this, {});
            this.choose_receipt_popup.appendTo(this.$el);

            this.error_negative_price_popup = new instance.point_of_sale.ErrorNegativePricePopupWidget(this, {});
            this.error_negative_price_popup.appendTo(this.$el);

            this.error_no_client_popup = new instance.point_of_sale.ErrorNoClientPopupWidget(this, {});
            this.error_no_client_popup.appendTo(this.$el);

            this.error_invoice_transfer_popup = new instance.point_of_sale.ErrorInvoiceTransferPopupWidget(this, {});
            this.error_invoice_transfer_popup.appendTo(this.$el);

           /* this.failure_action_popup = new module.FailureActionPopUpWidget(this, {});
            this.failure_action_popup.appendTo(this.$el);*/

            this.success_action_popup = new module.SuccessActionPopUpWidget(this, {});
            this.success_action_popup.appendTo(this.$el);



            this.new_customer_note_popup = new module.NotesPopupWidget(this, {pos:this.pos});
            this.new_customer_note_popup.appendTo(this.$el);

            // --------  Misc ---------

            this.close_button = new instance.point_of_sale.HeaderButtonWidget(this,{
                label: _t('Close'),
                action: function(){ self.close(); },
            });
            this.close_button.appendTo(this.$('.pos-rightheader'));

            this.notification = new instance.point_of_sale.SynchNotificationWidget(this,{});
            this.notification.appendTo(this.$('.pos-rightheader'));

            if(this.pos.config.use_proxy){
                this.proxy_status = new instance.point_of_sale.ProxyStatusWidget(this,{});
                this.proxy_status.appendTo(this.$('.pos-rightheader'));
            }

            this.username   = new instance.point_of_sale.UsernameWidget(this,{});
            this.username.replace(this.$('.placeholder-UsernameWidget'));

            this.customer_note = new module.NotesWidget(this,{});
            this.customer_note.replace(this.$('.placeholder-NotesWidget'));

            this.action_bar = new instance.point_of_sale.ActionBarWidget(this);
            this.action_bar.replace(this.$(".placeholder-RightActionBar"));

            this.left_action_bar = new instance.point_of_sale.ActionBarWidget(this);
            this.left_action_bar.replace(this.$('.placeholder-LeftActionBar'));

            this.paypad = new instance.point_of_sale.PaypadWidget(this, {});
            this.paypad.replace(this.$('.placeholder-PaypadWidget'));

            this.numpad = new instance.point_of_sale.NumpadWidget(this);
            this.numpad.replace(this.$('.placeholder-NumpadWidget'));

            this.order_widget = new instance.point_of_sale.OrderWidget(this, {});
            this.order_widget.replace(this.$('.placeholder-OrderWidget'));

            this.onscreen_keyboard = new instance.point_of_sale.OnscreenKeyboardWidget(this, {
                'keyboard_model': 'simple'
            });
            this.onscreen_keyboard.replace(this.$('.placeholder-OnscreenKeyboardWidget'));

            this.client_button = new instance.point_of_sale.HeaderButtonWidget(this,{
                label: _t('Self-Checkout'),
                action: function(){ self.screen_selector.set_user_mode('client'); },
            });
            this.client_button.appendTo(this.$('.pos-rightheader'));

            // --------  Screen Selector ---------

            this.screen_selector = new instance.point_of_sale.ScreenSelector({
                pos: this.pos,
                screen_set:{
                    'products': this.product_screen,
                    'payment' : this.payment_screen,
                    'client_payment' : this.client_payment_screen,
                    'scale_invite' : this.scale_invite_screen,
                    'scale':    this.scale_screen,
                    'receipt' : this.receipt_screen,
                    'welcome' : this.welcome_screen,
                },
                popup_set:{
                    'help': this.help_popup,
                    'error': this.error_popup,
                    'error-product': this.error_product_popup,
                    'error-session': this.error_session_popup,
                    'error-negative-price': this.error_negative_price_popup,
                    'choose-receipt': this.choose_receipt_popup,
                    'error-no-client': this.error_no_client_popup,
                    'error-invoice-transfer': this.error_invoice_transfer_popup,
                    /*'failure_action_popup':this.failure_action_popup,*/
                    'success_action_popup':this.success_action_popup,
                    'new_customer_note_popup':this.new_customer_note_popup,

                },
                default_client_screen: 'welcome',
                default_cashier_screen: 'products',
                default_mode: this.pos.config.iface_self_checkout ?  'client' : 'cashier',
            });

            if(this.pos.debug){
                this.debug_widget = new instance.point_of_sale.DebugWidget(this);
                this.debug_widget.appendTo(this.$('.pos-content'));
            }

            this.disable_rubberbanding();
        },
    });
}
