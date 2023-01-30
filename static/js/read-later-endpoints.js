const readLaterButtons = document.querySelectorAll('.read-later-btn');
readLaterButtons.forEach(button => {
    button.addEventListener('click', () => {
        const postId = button.getAttribute('data-post-id');
        let url, body, method;
        // add to read-later
        if (button.classList.contains("bi-bookmark")) {
            url = `/read-later/`;
            method = 'POST';
            body = JSON.stringify({ 'news': postId });
            button.querySelector("span").innerHTML = "Remove from Read-Later";
        }
        // remove from read-later
        else {
            url = `/read-later/` + postId;
            method = "delete"
            button.querySelector("span").innerHTML = "Add to Read-Later";
        }
        // Send the request
        fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json', "X-CSRFToken": csrftoken },
            body,

        }).then(response => {
            // if request is successful (action is performed)
            if (response.ok) {
                if (method === "delete") {
                    button.parentNode.parentNode.parentNode.style.display = "none";
                } else {
                    button.classList.toggle('bi-bookmark');
                    button.classList.toggle('bi-bookmark-fill');
                }
            } else {
                window.location.href = "/login";
            }
        })
    });
});
