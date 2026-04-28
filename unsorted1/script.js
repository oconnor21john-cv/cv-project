document.addEventListener('DOMContentLoaded', () => {
    // Password reveal functionality
    const togglePassword = document.getElementById('togglePassword');
    const password = document.getElementById('password');

    togglePassword.addEventListener('click', () => {
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        togglePassword.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
    });

    // Rest of your existing code...
    const loginForm = document.getElementById('loginForm');
    // ... existing code ...
}); 