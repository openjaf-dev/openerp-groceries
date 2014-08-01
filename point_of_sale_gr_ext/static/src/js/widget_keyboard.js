
function openerp_pos_keyboard_ext(instance, module){
    // ---------- OnScreen Keyboard Widget ----------

    // A Widget that displays an onscreen keyboard.
    // There are two options when creating the widget :
    //
    // * 'keyboard_model' : 'simple' | 'full' (default)
    //   The 'full' emulates a PC keyboard, while 'simple' emulates an 'android' one.
    //
    // * 'input_selector  : (default: '.searchbox input')
    //   defines the dom element that the keyboard will write to.
    //
    // The widget is initially hidden. It can be shown with this.show(), and is
    // automatically shown when the input_selector gets focused.

    module.OnscreenKeyboardGrWidget = instance.point_of_sale.OnscreenKeyboardWidget.include({
        start: function(){
            var self = this;

            $('.close_button').click(function(){
                self.deleteAllCharacters();
                self.hide();
            });

            $('.done_button').click(function(){
                self.hide();
            });

            // Keyboard key click handling
            $('.keyboard li').click(function(){

                var $this = $(this),
                    character = $this.html(); // If it's a lowercase letter, nothing happens to this variable

                if ($this.hasClass('left-shift') || $this.hasClass('right-shift')) {
                    self.toggleShift();
                    return false;
                }

                if ($this.hasClass('capslock')) {
                    self.toggleCapsLock();
                    return false;
                }

                if ($this.hasClass('delete')) {
                    self.deleteCharacter();
                    return false;
                }

                if ($this.hasClass('numlock')){
                    self.toggleNumLock();
                    return false;
                }

                // Special characters
                if ($this.hasClass('symbol')) character = $('span:visible', $this).html();
                if ($this.hasClass('space')) character = ' ';
                if ($this.hasClass('tab')) character = "\t";
                if ($this.hasClass('return')) character = "\n";

                // Uppercase letter
                if ($this.hasClass('uppercase')) character = character.toUpperCase();

                // Remove shift once a key is clicked.
                self.removeShift();

                self.writeCharacter(character);
            });
        },
        set_target:function(target){
            var self = this;
            this.$target = $(target);
        },
        disconnect : function(){
            var self = this;
            this.$target = null;
        },
    });
}
