$('.captcha').hover(function () {
    $(this).css('cursor', 'pointer');
}, function () {
    $(this).css('cursor', 'auto');
});

$('.captcha').click(function () {
    $('#id_captcha_1').val('');
    $('#id_captcha_1').css('visibility', 'hidden');
    $('.captcha').css('width', '50px');
    $('.captcha').attr('src', '/static/img/loading/loading.gif');
    $.getJSON("/captcha/refresh/", function (result) {
        $('.captcha').css('width', '50px');
        var image = new Image();
        image.src = result['image_url'];
        image.onload = function () {
            $('.captcha').css('width', '50px');
            $('.captcha').attr('src', result['image_url']);
            $('#id_captcha_0').val(result['key'])
            $('.captcha').css('width', '200px');
            $('#id_captcha_1').css('visibility', 'visible');
        };
    });
});