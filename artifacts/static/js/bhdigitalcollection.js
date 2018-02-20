$(function () {
    $('#filters').on('hidden.bs.collapse', function () {
        $('.filter-indicator').removeClass('clicked');
    }).on('show.bs.collapse', function () {
        $('.filter-indicator').addClass('clicked');
    });
    $('.origin-radio label').on('click', function (e) {
        e.preventDefault();
        var btn = $(this);
        var form = btn.parents('form');
        var formUrl = form.attr('action');
        btn.prop('disabled', true);
        $.ajax({
            url: formUrl,
            type: "GET",
            data: form.serializeArray(),
            success: function (data, textStatus, jqXHR) {
                $('#artifacts-list').html(data);
                btn.prop('disabled', false);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(errorThrown);
                btn.prop('disabled', false);
            }
        });
    });
});
