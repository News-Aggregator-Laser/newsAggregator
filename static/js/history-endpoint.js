const removeFromHistoryButtons = document.querySelectorAll('.history-remove-btn');
removeFromHistoryButtons.forEach(button => {
    button.addEventListener('click', event => {
        const postId = button.getAttribute('data-post-id');
        // Send the request
        fetch(`/history/${postId}`, {
            method: 'delete',
            headers: {'Content-Type': 'application/json', "X-CSRFToken": csrftoken},
            body: JSON.stringify({'news': postId}),

        })
            .then(response => {
                // if request is successful (action is performed)
                if (response.ok) {
                    button.parentNode.parentNode.parentNode.style.display = "none";
                }
            })
    });
});
