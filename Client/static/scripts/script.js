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
