// custom.js
document.addEventListener("DOMContentLoaded", function() {
    const sendButton = document.querySelector('.stButton button');
    const customSubmitButton = document.querySelector('#custom-submit-btn');

    if (sendButton && customSubmitButton) {
        customSubmitButton.addEventListener('click', function() {
            sendButton.click();
        });
    }
});
