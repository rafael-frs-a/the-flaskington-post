function activateCurrentNavitem() {
    var items = document.getElementsByClassName('nav-item');

    for (var i = 0; i < items.length; i++) {
        if (window.location.href.startsWith(items[i].querySelector('.nav-link').href)) {
            items[i].classList.add('active-nav-item');
            break
        }
    }
}

activateCurrentNavitem();

function toggleSortableHeader() {
    const urlParams = new URLSearchParams(window.location.search);
    const sort = urlParams.get('sort');

    if (!sort) {
        return;
    }

    header = document.querySelector(`[data-sort=${sort}]`);

    if (!header) {
        return;
    }

    desc = urlParams.get('desc');

    if (desc) {
        header.classList.add('th-sort-desc');
    }
    else {
        header.classList.add('th-sort-asc');
    }
}

toggleSortableHeader();

document.querySelectorAll('.th-sortable').forEach(header => {
    header.addEventListener('click', () => {
        const url = new URL(window.location.href);
        url.search = new URLSearchParams();
        const urlParams = new URLSearchParams(window.location.search);
        const page = urlParams.get('page');

        if (page) {
            url.searchParams.append('page', page);
        }

        url.searchParams.append('sort', header.dataset.sort);

        if (header.classList.contains('th-sort-asc')) {
            url.searchParams.append('desc', true);
        }

        window.location.href = url.href;
    });
});

$('#delete-modal').on('show.bs.modal', function(e) {
    const id = $(e.relatedTarget).data('row-id');
    const msg = $(e.relatedTarget).data('msg-id');
    $('#form-delete').attr('action', $('#form-delete').data('url-base') + '/' + id);
    $('#delete-modal-label').html(`Confirm deletion of ${msg}?`);
});
