
// this file contains the screens definitions. Screens are the
// content of the right pane of the pos, containing the main functionalities. 
// screens are contained in the PosWidget, in pos_widget.js
// all screens are present in the dom at all time, but only one is shown at the
// same time. 
//
// transition between screens is made possible by the use of the screen_selector,
// which is responsible of hiding and showing the screens, as well as maintaining
// the state of the screens between different orders.
//
// all screens inherit from ScreenWidget. the only addition from the base widgets
// are show() and hide() which shows and hides the screen but are also used to 
// bind and unbind actions on widgets and devices. The screen_selector guarantees
// that only one screen is shown at the same time and that show() is called after all
// hide()s

function openerp_pos_screens_ext(instance, module){ //module is instance.point_of_sale
    var QWeb = instance.web.qweb,
    _t = instance.web._t;

    // The NotesPopupWidget is the widget that contain all the data of a customer.

    module.NotesPopupWidget = instance.point_of_sale.PopUpWidget.extend({
        template: 'NotesPopupWidget',
        init: function(parent, options){
            var options = options || {};
            this._super(parent,options);
            this.pos = parent.pos;

        },
        show: function(){
            var self = this;
            this._super();

            this.$('#pop_cancel_button').off('click').click(function(){
                self.pos_widget.screen_selector.close_popup();
            });

            this.$('#pop_ok_button').off('click').click(function(){
                self.save_pop_note_data();
            });

        },
        bind2keyboard:function(selector){
            this.pos_widget.onscreen_keyboard.connect(this);
        },
        close: function(){
           /*this.el.querySelector('.searchbox input').addEventListener('click',function(event) {
                    self.pos_widget.onscreen_keyboard.connect(this);
            },false);*/
        },
        save_pop_note_data: function(option){
            var self = this;

            this.name = $(this.el.querySelector('#text1'))[0];
            this.phone = $(this.el.querySelector('#text2'))[0];
            this.note = $(this.el.querySelector('#text3'))[0];
            this.email = $(this.el.querySelector('#text4'))[0];            

            if (this.name.value != ''){
                data = {
                    'name':this.name.value,
                    'phone':this.phone.value,
                    'email':this.email.value,
                    'note':this.note.value
                }
                var partner = new instance.web.Model('res.partner');
				partner.call('create_from_ui',[data]).then(function(result){
					// TODO: set the client to the order
					//self.pos_widget.pos.get('selectedOrder').set('partner_id',result);
                });
                self.pos_widget.screen_selector.show_popup('success_action_popup');
            } else{
                this.pos_widget.screen_selector.show_popup('failure_action_popup');
            }
        },
    });

    // Modified to add popups.

    module.ScreenSelectorGr = instance.point_of_sale.ScreenSelector.include({
        add_popup: function(popup_name, popup){
            popup.hide();
            this.popup_set[popup_name] = popup;
        },
    });

    // The FailureActionPopUpWidget is the popup that shows when the customer note popup is not full filled.
    module.FailureActionPopUpWidget = instance.point_of_sale.ErrorPopupWidget.extend({
        template: 'FailureActionPopUpWidget',
        show: function(){
            var self = this;
            this._super();

            this.$('.footer .button').off('click').click(function(){
                self.pos_widget.screen_selector.show_popup('customer_note');
            });
        },
    });

    // The SuccessActionPopUpWidget is the popup that shows when the customer note data is sent successfully.

    module.SuccessActionPopUpWidget = instance.point_of_sale.ErrorPopupWidget.extend({
        template: 'SuccessActionPopUpWidget',
    });
}
