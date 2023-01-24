const readLaterButtons = document.querySelectorAll('.read-later-btn');
readLaterButtons.forEach(button => {
    button.addEventListener('click', event => {
        const postId = button.getAttribute('data-post-id');
        let url, body, method;
        if (button.classList.contains("bi-bookmark")) {
            url = `/read-later/`;
            method = 'POST';
            body = JSON.stringify({'news': postId});
        } else {
            url = `/read-later/` + postId;
            method = "delete"
        }
        fetch(url, {
            method,
            headers: {'Content-Type': 'application/json', "X-CSRFToken": csrftoken},
            body,

        })
            .then(response => response)
            .then(data => {
                // Update the UI with the new like count
                button.classList.toggle('bi-bookmark');
                button.classList.toggle('bi-bookmark-fill');
            });

    });
});
