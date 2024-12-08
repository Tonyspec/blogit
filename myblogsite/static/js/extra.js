document.addEventListener('DOMContentLoaded', function() {
    var modal = document.getElementById("commentModal");
    var btns = document.getElementsByClassName("toggle-comment");
    var span = document.getElementsByClassName("close-comment")[0];

    for (var i = 0; i < btns.length; i++) {
        btns[i].onclick = function(e) {
            e.preventDefault();
            var postId = this.getAttribute('data-post-id');
            
            // Update form action to point to the correct post detail
            var form = modal.querySelector('form');
            form.action = form.getAttribute('data-action');
            
            // Show modal
            modal.style.display = "block";
        }
    }

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});