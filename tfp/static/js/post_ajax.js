var formSubmitting = false;

function addImgAlt(html) {
    var parser = new DOMParser();
    var doc = parser.parseFromString(html, 'text/html');
    var images = doc.getElementsByTagName('img');

    for (var i = 0; i < images.length; i++) {
        if (!images[i].alt) {
            images[i].alt = 'Image from ' + images[i].src;
        }
    }

    return doc.documentElement.innerHTML;
}

$(document).ready(function() {
    $('form').on('submit', function(event) {
        event.preventDefault();
        var html = addImgAlt($('#summernote').summernote('code'));
        $('#summernote').summernote('code', html);

        $.ajax({
            data: $('form').serialize(),
            type: 'POST',
            url: window.location.pathname
        })

        .done(function(data) {
            if (data.success) {
                formSubmitting = true;
                window.location = $('#btn-home').attr('href');
            }
            else {
                $('#title-errors').find('span').remove();

                if (data.title_error) {
                    $('#title-input').addClass('is-invalid');
                    $('#title-errors').append('<span>' + data.title_error + '</span>');
                }
                else {
                    $('#title-input').removeClass('is-invalid');
                }

                $('#content-errors').find('small').remove();

                if (data.content_error) {
                    $('#content-container').addClass('invalid-post');
                    $('#content-errors').append('<small class="text-danger">' + data.content_error + '</small>');
                }
                else {
                    $('#content-container').removeClass('invalid-post');
                }

                window.scrollTo(0, 0);
            }
        });
    });
});

window.onbeforeunload = function(){
    if (formSubmitting) {
        formSubmitting = false;
        return undefined;
    }

    return 'Are you sure you want to leave this page?';
};
