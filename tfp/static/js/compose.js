$(document).ready(function() {
    $('#summernote').summernote({
        toolbar: [
            ['options', ['undo', 'redo']],
            ['style', ['style', 'bold', 'italic', 'underline', 'clear']],
            ['font', ['strikethrough', 'superscript', 'subscript']],
            ['color', ['backcolor']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['insert', ['link', 'picture']]
            // , ['misc', ['codeview']]
        ],
        shortcuts: false
    });

    $('#summernote').removeAttr('disabled');
    $('.loading-container').css('display', 'none');
});
