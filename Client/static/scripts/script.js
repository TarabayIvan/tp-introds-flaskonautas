const navLinks = document.getElementById("navLinks");

const showMenu = () => {
    navLinks.style.top = '0';
};

const hideMenu = () => {
    navLinks.style.top = '-800px';
};

document.getElementById('user-logo').addEventListener('click', (event) => {
    event.preventDefault();
    window.location.href = './user.html';
});