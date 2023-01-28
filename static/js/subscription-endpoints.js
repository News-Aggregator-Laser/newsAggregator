const subscriptionButton = document.getElementById('subscribe-button');
const email = document.getElementById('email-input');
subscriptionButton.addEventListener('click', () => {
    // Send the request
    fetch(`/subscription/`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({'email': email.value}),

    }).then(response => {
        // if request is successful (action is performed)
        if (response.ok) {
            email.disabled = true;
            email.style.background = "#00FF00";
            subscriptionButton.disabled = true;
        }else {
            email.style.background = "#FF0000";
        }
    })
});

