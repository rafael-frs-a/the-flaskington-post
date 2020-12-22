function openEditMenu(target) {
    var menu = null

    if (target.className === 'menu-edit-btn') {
        for (var i = 0; i < target.parentElement.children.length; i++) {
            if (target.parentElement.children[i].className === 'menu-edit-content') {
                menu = target.parentElement.children[i];
                break;
            }
        }
    }

    var menus = document.getElementsByClassName('menu-edit-content')

    for (var i = 0; i < menus.length; i++) {
        if (menus[i] != menu) {
            menus[i].style.display = 'none';
        }
    }

    if (menu != null) {
        if (menu.style.display === 'block') {
            menu.style.display = 'none';
        }
        else {
            menu.style.display = 'block';
        }
    }
}

$('.search-form').on('submit', function(event) {
    event.preventDefault();
    intersectionObserver.disconnect();

    if (sentinel) {
        sentinel.remove();
    }

    var no_post = document.querySelector('.container-msg');

    if (no_post) {
        no_post.remove();
    }

    var post_container = document.querySelector('.post-container');

    while (post_container) {
        post_container.remove();
        post_container = document.querySelector('.post-container');
    }

    sentinel_template = document.querySelector('#sentinel-template').content.cloneNode(true);
    document.body.appendChild(sentinel_template);
    sentinel = document.querySelector('#sentinel');
    page = 1;
    fetching = false;
    filter = document.querySelector('.nav-form-search').value;
    intersectionObserver.observe(sentinel);
});

window.addEventListener('mouseup', function(e) {
    if (e.target.className === 'menu-edit-btn') {
        return;
    }

    openEditMenu(e.target)
})

$('#delete-modal').on('show.bs.modal', function(e) {
    var title_slug = $(e.relatedTarget).data('post-id');
    $('#form-delete').attr('action', $('#form-delete').data('url-base') + '/' + title_slug);
})

var sentinel_template = document.querySelector('#sentinel-template').content.cloneNode(true);
document.body.appendChild(sentinel_template);

var posts_container = document.querySelector('#posts-container');
var post_template = document.querySelector('#post-template');
var no_post_template = document.querySelector('#no-post-template');
var menu_post_template = document.querySelector('#menu-post-template')
var sentinel = document.querySelector('#sentinel');
var page = 1;
var date = new Date();
var timezone = date.getTimezoneOffset();
var fetching = false;
var filter = '';

function loadPosts() {
    fetch(window.location.pathname + '?page=' + page.toString() + '&timezone=' + timezone.toString() + '&filter=' + filter).then((response) => {
        response.json().then((data) => {
            fetching = false;

            if (!data.posts.length) {
                var template = no_post_template.content.cloneNode(true);
                posts_container.appendChild(template);
                intersectionObserver.disconnect();
                sentinel.remove();
                return;
            }

            for (var i = 0; i < data.posts.length; i++) {
                var template = post_template.content.cloneNode(true);
                template.querySelector('.account-img-container').innerHTML = data.posts[i].author_img;
                template.querySelector('.post-title').innerHTML = data.posts[i].title;
                template.querySelector('.post-content').innerHTML = data.posts[i].content;
                template.querySelector('.post-author').innerHTML = data.posts[i].author;
                template.querySelector('.post-date').innerHTML = data.posts[i].date_posted;

                if (data.posts[i].date_edited) {
                    template.querySelector('.post-date-edited').innerHTML = data.posts[i].date_edited;
                }

                if (data.posts[i].is_author) {
                    var post_container = template.querySelector('.post-container');
                    var menu_template = menu_post_template.content.cloneNode(true);
                    menu_template.querySelector('.post-edit-link').href = data.posts[i].edit_url;
                    menu_template.querySelector('.post-delete-link').setAttribute('data-post-id', data.posts[i].title_slug);
                    post_container.appendChild(menu_template);
                }

                posts_container.appendChild(template);
            }

            page += 1;

            if (!data.has_next) {
                if (data.stop) {
                    sentinel.remove();
                }
                else {
                    sentinel.innerHTML = 'No more posts';
                }

                intersectionObserver.disconnect();
            }
        })
    })
}

var intersectionObserver = new IntersectionObserver(entries => {
    if (fetching || entries[0].intersectionRation <= 0) {
        return;
    }

    fetching = true;
    loadPosts();
});

intersectionObserver.observe(sentinel);
