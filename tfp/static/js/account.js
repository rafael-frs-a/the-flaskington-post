$('#delete-modal').on('show.bs.modal', function(e) {
    $('#form-delete').attr('action', $('#form-delete').data('url-base'));
})
