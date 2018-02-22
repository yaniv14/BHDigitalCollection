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
            data: {
                filter: form.find('input[name="filter"]').val(),
                is_private: form.find('input[name="is_private"]').val(),
                location: btn.find('input[type="radio"]').val()
            },
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
    $('#id_year_from,#id_year_to').on('change', function (e) {
        e.preventDefault();
        var input = $(this);
        var form = input.parents('form');
        var formUrl = form.attr('action');
        $.ajax({
            url: formUrl,
            type: "GET",
            data: {
                filter: form.find('input[name="filter"]').val(),
                is_private: form.find('input[name="is_private"]').val(),
                year_from: form.find('input[name="year_from"]').val(),
                year_to: form.find('input[name="year_to"]').val()
            },
            success: function (data, textStatus, jqXHR) {
                $('#artifacts-list').html(data);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(errorThrown);
            }
        });
    });
});
