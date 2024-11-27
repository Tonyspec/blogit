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