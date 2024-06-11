document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.getElementById("navLinks");

    document.getElementById('toggle-password').addEventListener('click', function() {
        var passwordElement = document.getElementById('password');
        if (passwordElement.classList.contains('hidden')) {
            passwordElement.classList.remove('hidden');
        } else {
            passwordElement.classList.add('hidden');
        }
    });

    const showMenu = () => {
        navLinks.style.top = '0';
    };

    const hideMenu = () => {
        navLinks.style.top = '-800px';
    };

    document.getElementById('user-logo').addEventListener('click', (event) => {
        event.preventDefault();
        window.location.href = './user';
    });
});


document.getElementById('searchInput').addEventListener('input', function(e) {
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


document.getElementById('post-image').addEventListener('change', function () {
    let size = this.files[0].size;
    if (size > 2 * 1024 * 1024) { // Limita el peso de la imagen a 2mb
      alert('El archivo es demasiado grande, el tamaño máximo permitido es de 2MB');
      this.value = '';
    };
  });