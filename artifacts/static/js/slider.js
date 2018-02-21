var range = document.getElementById('year-range');
var quick_years = document.getElementById('quick-years');

if (range !== null) {
    noUiSlider.create(range, {
        start: [1000, 1400],
        step: 50,
        connect: true,
        range: {
            'min': 0,
            'max': 2100
        },
        pips: {mode: 'count', values: 8}
    });

    range.noUiSlider.on('update', function (values, handle, unencoded, isTap, positions) {
        document.getElementById('id_year_from').value = Number(values[0]);
        document.getElementById('id_year_to').value = Number(values[1]);

        var event = new Event('change');
        document.getElementById('id_year_from').dispatchEvent(event);
        document.getElementById('id_year_to').dispatchEvent(event);

        // $('.form-filters form').find('input[name="year_from"]').val(values[0]);
        // $('.form-filters form').find('input[name="year_to"]').val(values[1]);
    });

    var handle = range.querySelector('.noUi-handle');

    handle.addEventListener('keydown', function (e) {

        var value = Number(range.noUiSlider.get());

        if (e.which === 37) {
            range.noUiSlider.set(value - 100);
        }

        if (e.which === 39) {
            range.noUiSlider.set(value + 100);
        }
    });

    var quick_buttons = quick_years.getElementsByTagName('button');

    for (i = 0; i < quick_buttons.length; i++) {
        quick_buttons[i].addEventListener('click', function (e) {

            var lower_value = Number(this.dataset.lower);
            var higher_value = Number(this.dataset.higher);

            range.noUiSlider.set([lower_value, higher_value]);
        });
    }
}


