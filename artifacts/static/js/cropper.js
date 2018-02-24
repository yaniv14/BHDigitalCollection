let crop_image = $('#id_image');
let cropBoxData;
let canvasData;
let sizeName;

$('#imageCropModal').on('shown.bs.modal', function (e) {
    let clickedBtn = e.relatedTarget;
    sizeName = clickedBtn.dataset.sizename;
    crop_image.cropper({
        viewMode: 1,
        aspectRatio: 1 / 1,
        minCropBoxWidth: Number(clickedBtn.dataset.width),
        minCropBoxHeight: Number(clickedBtn.dataset.height),
        ready: function () {
            crop_image.cropper('setCanvasData', canvasData);
            crop_image.cropper('setCropBoxData', cropBoxData);
        }
    });
}).on('click', '.get-crop-data', function (e) {
    cropBoxData = crop_image.cropper('getCropBoxData');
    canvasData = crop_image.cropper('getCanvasData');
    $('input[name="' + sizeName + '"]').val(JSON.stringify(canvasData));
    crop_image.cropper('destroy');
    $('#imageCropModal').modal('hide');
}).on('hidden.bs.modal', function () {
    crop_image.cropper('destroy');
});

// Enable zoom in button
$('.js-zoom-in').click(function () {
    crop_image.cropper('zoom', 0.1);
});

// Enable zoom out button
$('.js-zoom-out').click(function () {
    crop_image.cropper('zoom', -0.1);
});
