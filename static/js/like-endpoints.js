const likeButtons = document.querySelectorAll('.favorite-btn');
likeButtons.forEach(button => {
    button.addEventListener('click', () => {
        const postId = button.getAttribute('data-post-id');
        let url, body, method;
        // add to read-later
        if (button.classList.contains("bi-star")) {
            url = `/like/`;
            method = 'POST';
            body = JSON.stringify({'news': postId});
            button.querySelector("span").innerHTML = "Remove from favorite";
        }
        // remove from like
        else {
            url = `/like/` + postId;
            method = "delete"
            button.querySelector("span").innerHTML = "Add To favorite";
        }
        // Send the request
        fetch(url, {
            method,
            headers: {'Content-Type': 'application/json', "X-CSRFToken": csrftoken},
            body,

        }).then(response => {
            // if request is successful (action is performed)
            if (response.ok) {
                if (method === "delete"&&window.location.pathname==="/favorite/") {
                    button.parentNode.parentNode.parentNode.style.display = "none";
                } else {
                    button.classList.toggle('bi-star');
                    button.classList.toggle('bi-star-fill');
                }
            } else {
                window.location.href = "/login";
            }
        })
    });
});
