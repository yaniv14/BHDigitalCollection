$(function () {
    $('.top-links .dropdown').hover(function () {
        $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeIn(100);
    }, function () {
        $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeOut(100);
    });
    // Switch languages
    $('#lang-switcher a').click(function (e) {
        e.preventDefault();
        $('#id_language').val($(this).data('lang'));
        $('#lang-form').submit();
    });
});
