document.addEventListener('DOMContentLoaded', function () {

    load_all_posts();

    var urlParams = new URLSearchParams(window.location.search);
    page_no = urlParams.get('page');
    if (page_no === null) {
        document.getElementById('default_page').click();
    };

});

function load_all_posts() {

    const post_view = document.querySelectorAll('.feeds');
    let i = 0;
    let k = 0;

    fetch('/following_feeds')
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