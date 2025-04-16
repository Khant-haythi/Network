document.addEventListener('DOMContentLoaded', function() {
    const followForm = document.querySelector('#follow-form');
    const followButton = document.querySelector('#follow-btn');
    
    // Only sets color once when page loads
    if (followButton.textContent.trim() === 'Unfollow') {
        followButton.style.backgroundColor = '#ff5733'; // red
    } else {
        followButton.style.backgroundColor = '#6EC259'; // greeen
    }
    
});


function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, 9) === 'csrftoken=') {
                cookieValue = decodeURIComponent(cookie.substring(9));
                break;
            }
        }
    }
    return cookieValue;
}