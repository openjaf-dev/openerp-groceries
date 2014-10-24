function openerp_view_form_ext(instance, module){
    var QWeb = instance.web.qweb;
	var _t = instance.web._t;

    // Extension of FieldBinary template to change the max_upload_size from 25 to 150 MB.

    module.FieldBinaryExt = instance.web.form.FieldBinary.include({
        init: function(field_manager, node) {
            var self = this;
            this._super(field_manager, node);
            this.binary_value = false;
            this.useFileAPI = !!window.FileReader;
            this.max_upload_size = 150 * 1024 * 1024; // 25Mo
            if (!this.useFileAPI) {
                this.fileupload_id = _.uniqueId('oe_fileupload');
                $(window).on(this.fileupload_id, function() {
                    var args = [].slice.call(arguments).slice(1);
                    self.on_file_uploaded.apply(self, args);
                });
            }
        },
    });
}
