document.addEventListener('DOMContentLoaded', function() {
    let modal = document.getElementById("commentModal");
    let commentsContainer = document.getElementById("commentsContainer");
    let btn = document.querySelectorAll(".comment-btn");
    let span = document.getElementsByClassName("close")[0];
    let form = document.getElementById("newCommentForm");

    btn.forEach(button => {
        button.onclick = function(e) {
            e.preventDefault();
            modal.style.display = "block";
            let postId = this.getAttribute('data-post-id');
            form.setAttribute('data-post-id', postId); // Set post ID for form
            fetchComments(postId);
        }
    });

    span.onclick = function() {
        modal.style.display = "none";
    };

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        let postId = this.getAttribute('data-post-id');
        let commentText = this.elements['comment_text'].value;

        console.log('Comment Text:', commentText); // Log the comment text

        if (commentText.trim() === '') {
            console.warn('Comment is empty after trimming whitespace.');
            return;
        }

        fetch(`/blog/submit_comment/${postId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ 'comment_text': commentText })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.elements['comment_text'].value = '';
                fetchComments(postId);
            } else {
                console.error('Error submitting comment:', data.message);
            }
        });
    });

    function fetchComments(postId) {


        fetch(`/blog/fetch_comments/${postId}/`)
            .then(response => response.json())
            .then(data => {
                let commentsHTML = '';
                data.forEach(comment => {
                    commentsHTML += `<p>${comment.author.username}: ${comment.content} - ${new Date(comment.created_date).toLocaleString(undefined, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
})}</p>`;
                });
                commentsContainer.innerHTML = commentsHTML;
            });
    }

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('.post-image');
    images.forEach(image => {
        image.addEventListener('click', function() {
            if (document.fullscreenElement) {
                document.exitFullscreen();
            } else {
                image.requestFullscreen();
            }
        });
    });
});