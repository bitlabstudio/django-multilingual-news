(function($) {
    $(document).ready(function () {
        $('#id_title').bind('keyup change', function() {
            if (window.UNIHANDECODER) {
                value = UNIHANDECODER.decode($(this).val());
            }
            $('#id_slug').val(URLify($(this).val(), 64));
        });
    });
})(jQuery);