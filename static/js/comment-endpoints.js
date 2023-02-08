const commentsButtons = document.querySelectorAll('.delete-button');
commentsButtons.forEach(button => {
    button.addEventListener('click', () => {
        const commentId = button.getAttribute('comment-id');
        // Send the request
        fetch(`/comment/${commentId}`, {
            method: 'delete',
            headers: {'Content-Type': 'application/json', "X-CSRFToken": csrftoken},
            body: JSON.stringify({'news': commentId}),

        }).then(response => {
            // if request is successful (action is performed)
            if (response.ok) {
                button.parentNode.parentNode.style.display = "none";
            }
        })
    });
});
