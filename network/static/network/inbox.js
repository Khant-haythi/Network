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

function toggleLike(postId) {
    const likeButton = document.querySelector(`#like-btn-${postId}`);
    const heartIcon = document.querySelector(`#heart-icon-${postId}`);
    const likeCountElement = document.querySelector(`#like-count-${postId}`);

    fetch(`/like_post/${postId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            likeCountElement.textContent = data.likes;
            if (data.liked) {
                heartIcon.classList.remove('fa-regular');
                heartIcon.classList.add('fa-solid', 'text-success');
            } else {
                heartIcon.classList.remove('fa-solid', 'text-success');
                heartIcon.classList.add('fa-regular');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function getCsrfToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}