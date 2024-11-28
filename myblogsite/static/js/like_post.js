document.addEventListener('DOMContentLoaded', function() {
    const likeForms = document.querySelectorAll('.like-form');
    
    likeForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const likeButton = this.querySelector('.like-button');
            const likeCount = likeButton.querySelector('.like-count');
            
            fetch(this.action, {
                method: 'POST',
                body: new FormData(this),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.liked) {
                    likeButton.classList.add('liked');
                } else {
                    likeButton.classList.remove('liked');
                }
                likeCount.textContent = data.likes_count;
            });
        });
    });
    
});
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('.post img');
    
    images.forEach(img => {
        if (img.height > 300) { // or whatever max height you prefer
            img.style.height = '300px';
            img.style.width = 'auto'; // maintain aspect ratio
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Existing code for liking and image resizing...

    // Comment form toggle
    const toggleCommentButtons = document.querySelectorAll('.toggle-comment');
    
    toggleCommentButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const commentForm = this.nextElementSibling;
            if (commentForm) {
                commentForm.classList.toggle('hidden');
            }
        });
    });

    // Comment form submission (without AJAX for now, to ensure basic functionality)
    const commentForms = document.querySelectorAll('.comment-form');
    
    commentForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Here we don't prevent default because we want the form to submit normally
            // If you want to handle this with AJAX later, you would use e.preventDefault();
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var toggleCommentButton = document.querySelector('.toggle-comment');
    var commentPopup = document.getElementById('commentPopup');
    var closeCommentBtn = document.querySelector('.close-comment');

    if (toggleCommentButton && commentPopup && closeCommentBtn) {
        toggleCommentButton.onclick = function() {
            commentPopup.style.display = "block";
        };

        closeCommentBtn.onclick = function() {
            commentPopup.style.display = "none";
        };

        // Close if clicking outside
        window.onclick = function(event) {
            if (event.target == commentPopup) {
                commentPopup.style.display = "none";
            }
        };
    }
});