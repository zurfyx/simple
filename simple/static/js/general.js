(function() {
    function contentResize() {
        var header = $('header');
        var footer = $('footer');
        var menu = $('#menu');
        var totalHeight = header.outerHeight() + menu.outerHeight() + footer.outerHeight();
        var remainingHeight = window.innerHeight - totalHeight;
        $('#content').css('min-height', remainingHeight + 'px');
    }

    ///

    contentResize();
})(jQuery);