
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
            this.partner_id = false;
            var self = this;
        },
        validate_form_popup:function(e){
             // Declare the function variables:
            // Parent form, form URL, email regex and the error HTML
            var $formId = $('#pop_ok_button').parents('form');
            var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
            var numericReg = /\+?(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*(\d{1,2})$/;
            var characterReg = /^\s*[a-zA-Z,\s]+\s*$/;
            var $error = $('<span class="error"></span>');

            // Prepare the form for validation - remove previous errors
            $('li',$formId).removeClass('error');
            $('span.error').remove();

            // Validate all inputs with the class "required"
            $('.required',$formId).each(function(){
                var inputVal = $(this).val();
                var $parentTag = $(this).parent();
                // Run the name validation using the regex for those input items also having class "name"
                if($(this).hasClass('name') == true){
                    if(inputVal == ''){
                        $parentTag.addClass('error').append($error.clone().text('Required Field'));
                    }else if(!characterReg.test(inputVal)){
                        $parentTag.addClass('error').append($error.clone().text('Enter valid name'));
                    }
                }

                // Run the phone validation using the regex for those input items also having class "phone"
                if($(this).hasClass('phone') == true){
                    if(inputVal == ''){

                    }else if(!numericReg.test(inputVal)){
                        $parentTag.addClass('error').append($error.clone().text('Enter valid phone number'));
                    }
                }

                // Run the email validation using the regex for those input items also having class "email"
                if($(this).hasClass('email') == true){
                    if(!emailReg.test(inputVal)){
                        $parentTag.addClass('error').append($error.clone().text('Enter valid email'));
                    }
                }
            });

            // All validation complete - Check if any errors exist
            // If has errors
            if ($('span.error').length > 0) {

                $('span.error').each(function(){

                    // Set the distance for the error animation
                    var distance = 5;

                    // Get the error dimensions
                    var width = $(this).outerWidth();

                    // Calculate starting position
                    var start = width + distance;

                    // Set the initial CSS
                    $(this).show().css({
                        display: 'block',
                        opacity: 0,
                        right: -start+'px'
                    })
                    // Animate the error message
                    .animate({
                        right: -width+'px',
                        opacity: 1
                    }, 'slow');

                });
            } else {

                e.stopPropagation()
                // Prevent form submission
                e.preventDefault();
                this.save_pop_note_data();
            }
        },
        load_data: function(model, fields, domain){
            return new instance.web.Model(model).query(fields).filter(domain).all();
        },
        initial_config: function(){
            var self = this;

            $('body').off('keyup').on('keyup',function(e){
                if(e.which === 13){
                   self.validate_form_popup(e);
                }else if (e.which === 27){
                    self.pos_widget.screen_selector.close_popup();
                }else if(e.which === 78){
                    self.pos_widget.screen_selector.show_popup('new_customer_note_popup');
                }
            });

            this.$('#name').on('keypress',function(e){
                if(e.which != 0){
                    self.partner_id = false;
                }
            });

            this.$('#name').focus();

            this.$('#pop_cancel_button').off('click').click(function(){
                self.pos_widget.screen_selector.close_popup();
            });

            var map = {};

            this.$('#name').typeahead({
                source: function(query, process){
                  var names = [];
                  var partners = self.load_data('res.partner', ['id','name','mobile','email'], [['customer','=',true], ['company_id', '=', self.pos_widget.pos.company.id]])
                        .then(function(partners){
                          $.each(partners, function(i, partner){
							 map[partner.name ] = partner;
							 names.push(partner.name);
                          });
                          process(names);
                      });
                },
                updater: function (item) {
					partner = map[item];
                    self.partner_id = partner.id;
                    var mobile = partner.mobile;
                    var email = partner.email;
                    if (mobile != '' || mobile != false){
                        self.$('#phone')[0].value = mobile;
                    }
                    if (email != '' || email != false){
                        self.$('#email')[0].value = email;
                    }
                    return item;
                },
            });
            this.$('#name')[0].value= "";
            this.$('#phone')[0].value= "";
            this.$('#email')[0].value= "";
            this.$('#note')[0].value= "";

            // Fade out error message when input field gains focus
            $('.required').focus(function(){
                var $parent = $(this).parent();
                $parent.removeClass('error');
                $('span.error',$parent).fadeOut();
            });

            var $formId = $(this).parents('form');
            $('li',$formId).removeClass('error');
		    $('span.error').remove();
        },
        conf_button_ok: function(){
            var self = this;
            $('#pop_ok_button').off('click').click(function(e){
                self.validate_form_popup(e);
            });
        },
        show: function(){
            var self = this;
            this._super();

            this.initial_config();
            this.conf_button_ok();
        },
        bind2keyboard:function(selector){
            this.pos_widget.onscreen_keyboard.connect(this);
        },
        close: function(){
        },
        save_pop_note_data: function(option){
            var self = this;
            var name = $(this.el.querySelector('#name'))[0];
            var phone = $(this.el.querySelector('#phone'))[0];
            var note = $(this.el.querySelector('#note'))[0];
            var email = $(this.el.querySelector('#email'))[0];

            data = {
                'name':name.value,
                'phone':phone.value,
                'email':email.value,
                'note': note.value,
                'id':this.partner_id
            }
            var partner = new instance.web.Model('res.partner')
            partner.call('create_from_ui',[data]).then(function(result){
                var client = {'id':result,'name':name.value}
                self.pos.get('selectedOrder').set_client(client);
				self.pos_widget.screen_selector.show_popup('success_action_popup');
            });
        },
    });

    // Modified to add popups.

    module.ScreenSelectorGr = instance.point_of_sale.ScreenSelector.include({
        add_popup: function(popup_name, popup){
            popup.hide();
            this.popup_set[popup_name] = popup;
        },
    });

    // The SuccessActionPopUpWidget is the popup that shows when the customer note data is sent successfully.

    module.SuccessActionPopUpWidget = instance.point_of_sale.ErrorPopupWidget.extend({
        template: 'SuccessActionPopUpWidget',
        show: function(){
            var self = this;
            this._super();

            $('body').off('keyup').on('keyup',function(e){
                if(e.which === 13){

                }else if(e.which === 27){
                   self.pos_widget.screen_selector.close_popup();
                }else if(e.which === 78){
                    self.pos_widget.screen_selector.show_popup('new_customer_note_popup');
                }
            });

            this.$('#pop_cancel_button1').click(function(){
                self.pos_widget.screen_selector.close_popup();
            });
        },
        close: function(){
        },
    });

    module.PaymentScreenWidgetGr = instance.point_of_sale.PaymentScreenWidget.include({
        level:1,
        load_data: function(model, fields, domain){
            return new instance.web.Model(model).query(fields).filter(domain).all();
        },
        get_card_image_url: function(card){
            return window.location.origin + '/web/binary/image?model=pos.credit.cards.conf&field=image&id='+card;
        },
        render_cards: function(line){
            var card_arr = new Array();
            var cards_json = line.cashregister.journal.credit_cards_json_str.split(',');
            if(cards_json.length != 0){
                for(var i = 0; i < cards_json.length; i++){
                    if (cards_json[i] != ''){
                        var card = cards_json[i].split(':');
                        card_arr[(card[1]+'_'+this.level).replace(/ /i,'')] = this.get_card_image_url(card[0]);
                    }
                }
            }
            this.level++;
            return card_arr;
        },
        render_paymentline: function(line){
            var journal_type = line.cashregister.journal.type = line.cashregister.journal.type;
            var el_html;
            if (journal_type != 'cash'){
                el_html  = openerp.qweb.render('Paymentline',{widget: this, line: line, cards: this.render_cards(line)});
            }else{
                el_html  = openerp.qweb.render('Paymentline',{widget: this, line: line});
            }

            el_html  = _.str.trim(el_html);

            var el_node  = document.createElement('tbody');
                el_node.innerHTML = el_html;
                el_node = el_node.childNodes[0];
                el_node.line = line;
            var paymentline_delete;
            if (journal_type != 'cash'){
                paymentline_delete = el_node.querySelector('.paymentline-delete1');
            }else{
                paymentline_delete = el_node.querySelector('.paymentline-delete');
            }

            paymentline_delete.addEventListener('click', this.line_delete_handler);

            el_node.addEventListener('click', this.line_click_handler);

            var input = el_node.querySelector('input');
            if (input !=null){
                input.addEventListener('keyup', this.line_change_handler);
            }

            var radio_node_list = el_node.querySelectorAll('input[type=radio]');
            for(var i = 0; i < radio_node_list.length; i++){
                radio_node_list[i].addEventListener('click',this.radio_checked);
            }

            line.node = el_node;

//            if (journal_type != 'cash'){
//                $('.payment-info').hide();
//            }else{
//                $('.payment-info').show();
//            }

            return el_node;
        },
        radio_checked:function(){
            var self = this;
            $(':radio').not('[name*='+self.name+']').each(function(thais){
                $(this).attr("checked",false);
            });
        },
    });
}
