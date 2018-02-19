$(function () {
    $('#filters').on('hidden.bs.collapse', function () {
        $('.filter-indicator').removeClass('clicked');
    }).on('show.bs.collapse', function () {
        $('.filter-indicator').addClass('clicked');
    })
});
