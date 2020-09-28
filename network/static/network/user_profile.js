document.addEventListener('DOMContentLoaded', function () {

    const logged_user = document.querySelector('#login_user').innerHTML;
    const username = document.querySelector('#user-profile').innerHTML;
    load_follow(username);
    load_post(username);

    var urlParams = new URLSearchParams(window.location.search);
    page_no = urlParams.get('page');
    if (page_no === null) {
        document.getElementById('default_page').click();
    };
    if (username != logged_user) {

        document.querySelector('.follow_bt').addEventListener('click', () => follow_view(username));
    }




});


function load_post(user_id) {

    document.querySelector('#edit_view').style.display = 'none';
    document.querySelector('#post_view').style.display = 'block';

    const edit_view = document.querySelectorAll('#feeds');
    const post_view = document.querySelectorAll('.feeds');
    let i = 0;
    let j = 0;
    let k = 0;

    fetch(`/feeds/${user_id}`)
        .then(response => response.json())
        .then(result => {
            console.log(result)

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
            const like_button = new_result.map(user => {
                if (likers_array[k].length === 0) {
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
                }
            });
            console.log(like_button);

            const no_likes = new_result.map(user => {
                return user.no_of_likes
            });

            console.log(no_likes);
            post_view.forEach(feeds => {
                feeds.querySelector('#like_count').innerHTML = no_likes[j];
                feeds.querySelector('#like_div').innerHTML = like_button[j];
                j++;
            })
        });

};


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
            const username = document.querySelector('#user-profile').innerHTML;
            load_post(username);
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
                    const username = document.querySelector('#user-profile').innerHTML;
                    load_post(username);
                });
        });
};



function load_follow(user_name) {

    fetch(`/follows/${user_name}`)
        .then(response => response.json())
        .then(result => {
            console.log(result);
            document.querySelector('#followers_num').innerHTML = result.no_of_followers;
            document.querySelector('#followings_num').innerHTML = result.no_of_followings;

            const login_user = document.querySelector('#login_user').innerHTML;
            console.log(login_user);
            const follower = result.followers;
            console.log(follower)

            if (follower.length === 0) {
                document.querySelector('.follow_bt').innerHTML = "Follow";

            }
            else {
                for (var i = 0; i < follower.length; i++) {

                    if (login_user === follower[i]) {

                        document.querySelector('.follow_bt').innerHTML = "UnFollow";
                        break;
                    }
                    else {
                        document.querySelector('.follow_bt').innerHTML = "Follow";

                    }
                };
            }
        });

};


function follow_view(user_name) {

    fetch(`/follows/${user_name}`)
        .then(response => response.json())
        .then(result => {
            console.log(result);
            let no_of_follower = result.no_of_followers;
            no_of_follower++;


            fetch(`/follows/${user_name}`, {
                method: "PUT",
                body: JSON.stringify({
                    no_of_followers: no_of_follower
                })
            })
                .then(() => {
                    const username = document.querySelector('#user-profile').innerHTML;
                    load_follow(username);
                    load_post(username);

                })

        });



};
