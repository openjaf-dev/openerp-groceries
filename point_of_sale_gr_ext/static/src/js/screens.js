
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

            /* var self = this;*/

            /*if(this.pos.config.iface_vkeyboard && this.pos_widget.onscreen_keyboard){
                this.el.querySelector('#text1').addEventListener('click',function(event) {
                    self.pos_widget.onscreen_keyboard.connect(this);
                },false);

               this.el.querySelector('#text2').addEventListener('click',function(event) {
                    self.pos_widget.onscreen_keyboard.connect(this);
                },false);

               this.el.querySelector('#text3').addEventListener('click',function(event) {
                    self.pos_widget.onscreen_keyboard.connect(this);
                },false);
            }*/

        },
        show: function(){
            var self = this;
            this._super();

            this.$('#pop_cancel_button').off('click').click(function(){
                self.pos_widget.screen_selector.close_popup();
            });

            /*this.$('#pop_ok_button').off('click').click(function(){
               *//* var emailReg = new RegExp(/(^|\s):((\w)*)/g);*//*
                self.save_pop_note_data();
            });*/

            var colors = ['amarillo','verde', 'violeta', 'azul'];
            this.$('#name').typeahead({
                source:colors/*function(query, process){
                  var names = [];
                  var partners = new instance.web.Model('res.partner').query(['name','email','mobile']).filter([['customer','=',true]]).context('').all();
                  alert(partners[0].name);
                    var map = {};
                  $.each(partners,function(i, partner){
                     map[partner.name] = partner;
                     names.push(partner.name);
                  });

                  process(names);
                }*/,
            });

            this.$('#name')[0].value= "";
            this.$('#phone')[0].value= "";
            this.$('#email')[0].value= "";
            this.$('#note')[0].value= "";

            var $formId = $(this).parents('form');
            $('li',$formId).removeClass('error');
		    $('span.error').remove();

            ///
            $('#pop_ok_button').off('click').click(function(e){

                // Declare the function variables:
                // Parent form, form URL, email regex and the error HTML
                var $formId = $(this).parents('form');
                var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
                var numericReg = /^\d*[0-9](|.\d*[0-9]|,\d*[0-9])?$/;
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
                    self.save_pop_note_data();
                }
                // Prevent form submission
                e.preventDefault();
            });

            // Fade out error message when input field gains focus
            $('.required').focus(function(){
                var $parent = $(this).parent();
                $parent.removeClass('error');
                $('span.error',$parent).fadeOut();
            });


             /*if(this.pos.config.iface_vkeyboard && this.pos_widget.onscreen_keyboard){


                *//*this.el.querySelector('#text1').addEventListener('click',function(event) {
                    self.pos_widget.onscreen_keyboard.connect(this);
                },false);

               this.el.querySelector('#text2').addEventListener('click',function(event) {
                    self.pos_widget.onscreen_keyboard.connect(this);
                },false);

               this.el.querySelector('#text3').addEventListener('click',function(event) {
                    self.pos_widget.onscreen_keyboard.connect(this);
                },false);*//*





                *//*this.pos_widget.onscreen_keyboard.connect($(this.el.querySelector('#text2')));
                this.pos_widget.onscreen_keyboard.connect($(this.el.querySelector('#text3')));*//*

                *//*this.el.querySelector('#text1').addEventListener('click',this.conect2keyboard('#text1'));
                this.el.querySelector('#text2').addEventListener('click',this.conect2keyboard1('#text2'));
                this.el.querySelector('#text3').addEventListener('click',this.conect2keyboard2('#text3'));*//*

               *//* this.$('#text1').click(function(){
                    //self.pos_widget.onscreen_keyboard.set_target($(self.el.querySelector('#text1')));
                    self.pos_widget.onscreen_keyboard.connect($(self.el.querySelector('#text1')));
                });*//*
                *//*this.$('#text2').click(function(){
                   // self.pos_widget.onscreen_keyboard.set_target($(self.el.querySelector('#text2')));
                    self.pos_widget.onscreen_keyboard2.connect($(self.el.querySelector('#text2')));
                });
                this.$('#text3').click(function(){
                    //self.pos_widget.onscreen_keyboard.set_target($(self.el.querySelector('#text3')));
                    self.pos_widget.onscreen_keyboard3.connect($(self.el.querySelector('#text3')));
                });*//*



                *//* this.$el.find('#text1').click(_.bind(this.conect2keyboard, this));
                 this.$el.find('#text2').click(_.bind(this.conect2keyboard1, this));*//*
            }*/
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

            var name = $(this.el.querySelector('#name'))[0];
            var phone = $(this.el.querySelector('#phone'))[0];
            var note = $(this.el.querySelector('#note'))[0];
            var email = $(this.el.querySelector('#email'))[0];

            /*this.session_id = this.pos_widget.pos.pos_session.id*/

            /*if (this.name.value != ''){*/
            /*this.timeout = 7500;*/

            data = {
                'name':name.value,
                'phone':phone.value,
                'email':email.value,
                'note': note.value/*,
                'pos_session_id':this.session_id*/
            }

             var partner = new instance.web.Model('res.partner')

             partner.call('create_from_ui',[data]).then(function(result){
                  /*alert(result);*/
                 var client = {'id':result,'name':name.value}
                 self.pos.get('selectedOrder').set_client(client);
              });

            self.pos_widget.screen_selector.show_popup('success_action_popup');
            /*}else{
                this.pos_widget.screen_selector.show_popup('failure_action_popup');
            }*/
        },
    });

    // Modified to add popups.

    module.ScreenSelectorGr = instance.point_of_sale.ScreenSelector.include({
        add_popup: function(popup_name, popup){
            popup.hide();
            this.popup_set[popup_name] = popup;
        },
    });

   /* // The FailureActionPopUpWidget is the popup that shows when the customer note popup is not full filled.
    module.FailureActionPopUpWidget = instance.point_of_sale.ErrorPopupWidget.extend({
        template: 'FailureActionPopUpWidget',
        show: function(){
            var self = this;
            this._super();

            this.$('#pop_cancel_button1').click(function(){
                self.pos_widget.screen_selector.show_popup('customer_note');
            });
        },
    });*/

    // The SuccessActionPopUpWidget is the popup that shows when the customer note data is sent successfully.

    module.SuccessActionPopUpWidget = instance.point_of_sale.ErrorPopupWidget.extend({
        template: 'SuccessActionPopUpWidget',
        show: function(){
            var self = this;
            this._super();

            this.$('#pop_cancel_button1').click(function(){
                self.pos_widget.screen_selector.close_popup();
            });
        },
    });
}
