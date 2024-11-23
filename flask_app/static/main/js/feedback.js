// Handles feedback toggling

document.addEventListener('DOMContentLoaded', function() {
    const feedbackButton = document.getElementById('feedback-button');
    const feedbackFormOverlay = document.getElementById('feedback-form-overlay');

    feedbackButton.addEventListener('click', function() {
        feedbackFormOverlay.classList.toggle('hidden');
    });

    // Close the form when clicking outside of it
    feedbackFormOverlay.addEventListener('click', function(event) {
        if (event.target === feedbackFormOverlay) {
            feedbackFormOverlay.classList.add('hidden');
        }
    });
});