document.addEventListener('DOMContentLoaded', function() {
   
    const followButton = document.querySelector('#follow-btn');
    
    // Only sets color once when page loads
    if (followButton.textContent.trim() === 'Unfollow') {
        followButton.style.backgroundColor = '#ff5733'; // red
    } else {
        followButton.style.backgroundColor = '#6EC259'; // greeen
    }
    


});

function editPost(postId) {
    console.log('postId:', postId); // Debug: Verify postId
    const postContent = document.querySelector(`#post-content-${postId}`);
    const postTextArea = document.querySelector(`#post-textarea-${postId}`);
    const editButton = document.querySelector(`#edit-post-btn-${postId}`);

    // Check if elements exist
    if (!postContent || !postTextArea || !editButton) {
        console.error(`Missing elements: postContent=${!!postContent}, postTextArea=${!!postTextArea}, editButton=${!!editButton}`);
        alert('Error: Post elements not found');
        return;
    }

    // Toggle between Edit and Save modes
    if (editButton.textContent === 'Edit') {
        // Switch to edit mode
        const originalContent = postContent.textContent;
        postTextArea.value = originalContent;
        postContent.style.display = 'none';
        postTextArea.style.display = 'block';
        editButton.textContent = 'Save';
    } else {
        // Switch to save mode
        const newContent = postTextArea.value.trim();
        if (newContent === '') {
            alert('Post content cannot be empty');
            return;
        }
        savePost(postId);
    }
}

function savePost(postId) {
    const content = document.querySelector(`#post-textarea-${postId}`).value;

    fetch(`/edit_post/${postId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ content: content }),
    })
    .then(response => {
       return response.json();
    })
    .then(data => {
             // Debug success response
            const postContent = document.querySelector(`#post-content-${postId}`);
            const postTextArea = document.querySelector(`#post-textarea-${postId}`);
            const editButton = document.querySelector(`#edit-post-btn-${postId}`);
            
            postContent.textContent = data.updated_content; 
            postContent.style.display = 'block';
            postTextArea.style.display = 'none';
            editButton.textContent = 'Edit';
           
        } 
            )
    .catch(error => {
        console.error('Detailed error:', error); // Debug detailed error
        alert('Error saving post. Please check the console for details.');
    });
}

function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) {
            return value;
        }
    }
    return null;
}