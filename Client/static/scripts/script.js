document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.getElementById("navLinks");
    const togglePassword = document.getElementById('toggle-password');
    const userLogo = document.getElementById('user-logo');
    const searchInput = document.getElementById('searchInput');
    const postImage = document.getElementById('post-image');

    window.showMenu = function() {
        navLinks.style.top = '0';
    };

    window.hideMenu = function() {
        navLinks.style.top = '-800px';
    };

    if (togglePassword) {
        togglePassword.addEventListener('click', function() {
            var passwordElement = document.getElementById('password');
            if (passwordElement.classList.contains('hidden')) {
                passwordElement.classList.remove('hidden');
            } else {
                passwordElement.classList.add('hidden');
            }
        });
    }

    if (userLogo) {
        userLogo.addEventListener('click', (event) => {
            event.preventDefault();
            window.location.href = './user';
        });
    }

    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            let searchValue = e.target.value.toLowerCase();
            let posts = document.getElementsByClassName('card');

            for (let i = 0; i < posts.length; i++) {
                let post = posts[i];
                let postTitle = post.getAttribute('data-title');

                if (postTitle.indexOf(searchValue) > -1) {
                    post.style.display = '';
                } else {
                    post.style.display = 'none';
                }
            }
        });
    }

    if (postImage) {
        postImage.addEventListener('change', function () {
            let size = this.files[0].size;
            if (size > 2 * 1024 * 1024) { // Limita el peso de la imagen a 2mb
                alert('El archivo es demasiado grande, el tamaño máximo permitido es de 2MB');
                this.value = '';
            };
        });
    }
});
