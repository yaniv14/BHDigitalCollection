let crop_image = $('#id_image');
let cropBoxData;
let canvasData;
let cropData;
let sizeName;
let currentData;
let clickedBtn;

$('#imageCropModal').on('shown.bs.modal', function (e) {
    clickedBtn = e.relatedTarget;
    sizeName = clickedBtn.dataset.sizename;
    currentData = $('input[name="' + sizeName + '"]').val();
    crop_image.cropper({
        viewMode: 1,
        aspectRatio: Number(clickedBtn.dataset.width) / Number(clickedBtn.dataset.height),
        dragMode: 'move',
        data: currentData,
        // minCropBoxWidth: Number(clickedBtn.dataset.width),
        // minCropBoxHeight: Number(clickedBtn.dataset.height),
        // ready: function () {
        //     crop_image.cropper('setCanvasData', canvasData);
        //     crop_image.cropper('setCropBoxData', cropBoxData);
        // }
    });
}).on('click', '.get-crop-data', function (e) {
    cropBoxData = crop_image.cropper('getCropBoxData');
    canvasData = crop_image.cropper('getCanvasData');
    cropData = crop_image.cropper('getData');
    $('input[name="' + sizeName + '"]').val(JSON.stringify(cropData));
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
