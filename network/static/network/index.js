document.addEventListener('DOMContentLoaded', function () {

    load_all_posts();

    var urlParams = new URLSearchParams(window.location.search);
    page_no = urlParams.get('page');
    if (page_no === null) {
        document.getElementById('default_page').click();
    };

    document.querySelector('.feed_bt').disabled = true;
    document.querySelector('#new_text').onkeyup = () => {
        if (document.querySelector('#new_text').value.length > 0) {
            document.querySelector('.feed_bt').disabled = false;
        }
        else {
            document.querySelector('.feed_bt').disabled = true;
        }
    };


});


function load_edit(feed_id) {
    document.querySelector('#post_view').style.animationPlayState = 'running';
    document.querySelector('#edit_view').style.animationPlayState = 'running';
    document.querySelector('#post_view').addEventListener('animationend', () => {
        document.querySelector('#post_view').style.display = 'none';
        document.querySelector('#edit_view').style.display = 'block';

    });

    fetch(`/feeds/${feed_id}`)
        .then(response => response.json())
        .then(result => {
            console.log(result);
            document.querySelector('#edit_text').value = result.text;
            document.querySelector('#save_div').innerHTML = `<button id="save_bt" onclick="save_edit(${result.id})">Save</button>`
        });

};

function save_edit(save_id) {

    fetch(`/feeds/${save_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            text: document.querySelector('#edit_text').value
        })
    })
        .then(() => {
            load_all_posts();
        });

};

function load_all_posts() {

    document.querySelector('#post_view').style.display = 'block';
    document.querySelector('#edit_view').style.display = 'none';

    const post_view = document.querySelectorAll('.feeds');
    let i = 0;
    let k = 0;

    fetch('/feeds')
        .then(response => response.json())
        .then(result => {
            console.log(result);

            var urlParams = new URLSearchParams(window.location.search);
            page_no = urlParams.get('page');
            const x = (page_no * 5) - 5;
            const new_result = result.splice(x, 5);
            console.log(new_result);


            const likers_array = new_result.map(user => {
                return user.likes
            })
            console.log(likers_array);

            const login_user = document.querySelector('#login_user').innerHTML;
            console.log(login_user);
            const like_button = new_result.map(user => {
                if (likers_array[k].length == 0) {
                    k++;
                    return `<button onclick="like_post(${user.id})" class="like_bt">Like</button>`;
                }
                else {
                    for (var a = 0; a < likers_array[k].length; a++) {
                        if (login_user === likers_array[k][a]) {
                            k++;
                            return `<button onclick="like_post(${user.id})" class="like_bt">Unlike</button>`;
                        }
                    }
                    k++;
                    return `<button onclick="like_post(${user.id})" class="like_bt">Like</button>`;
                };
            });

            const no_likes = new_result.map(user => {
                return user.no_of_likes
            });

            console.log(like_button);
            console.log(no_likes);

            post_view.forEach(feeds => {
                feeds.querySelector('#like_div').innerHTML = like_button[i];
                feeds.querySelector('#like_count').innerHTML = no_likes[i];
                i++;
            });
        });

};

function like_post(feed_id) {

    fetch(`/feeds/${feed_id}`)
        .then(response => response.json())
        .then(result => {
            console.log(result);
            let like = result.no_of_likes;
            like++;

            console.log(like);

            fetch(`/feeds/${feed_id}`, {
                method: "PUT",
                body: JSON.stringify({
                    no_of_likes: like
                })
            })
                .then(() => {
                    load_all_posts();
                });
        });
};
