function checkRows(event) {
    document.querySelectorAll('.td-check').forEach(cb => {
        cb.checked = event.target.checked;
    });
}

document.querySelectorAll('.cell-checkbox').forEach(cell => {
    cell.addEventListener('click', () => {
        const checkbox = cell.querySelector('input[type=checkbox]');

        if (!checkbox) {
            return;
        }

        checkbox.checked = !checkbox.checked;

        if (checkbox.classList.contains('th-check')) {
            const evt = document.createEvent("HTMLEvents");
            evt.initEvent("change", false, true);
            checkbox.dispatchEvent(evt);
        }
    });
});

const checkbox = document.querySelector('.th-check');

if (checkbox) {
    checkbox.addEventListener('change', (event) => {
        checkRows(event);
    })
}

$('#delete-selected-modal').on('show.bs.modal', function(e) {
    var email_ids = [];

    document.querySelectorAll('.td-check').forEach(cb => {
        if (cb.checked) {
            email_ids.push(cb.dataset.id);
        }
    });

    if (email_ids.length == 0) {
        $('#form-delete-selected').hide();
        $('#delete-selected-modal-label').html('No email selected.');
    }
    else {
        $('#form-delete-selected').show();
        $('#form-delete-selected').attr('action', $('#form-delete-selected').data('url-base') + '/' + email_ids.join());
        $('#delete-selected-modal-label').html(`Confirm deletion of the ${email_ids.length} emails selected?`);
    }
});
