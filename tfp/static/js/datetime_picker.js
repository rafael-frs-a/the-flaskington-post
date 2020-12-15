$('.datetimepicker').datetimepicker({
    format: 'm/d/Y H:i',
    step: 5
});

$('.datetimepicker-icon').click(function() {
    $('.datetimepicker').focus();
});
