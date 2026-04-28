
function validateEmail(email) {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}$/;
    return emailPattern.test(email);
}
function showError(input, message) {
    const errorElement = document.getElementById(`${input.id}-error`);
    if (errorElement) errorElement.textContent = message;
    input.setAttribute('aria-invalid', 'true');
}
function clearError(input) {
    const errorElement = document.getElementById(`${input.id}-error`);
    if (errorElement) errorElement.textContent = '';
    input.setAttribute('aria-invalid', 'false');
}
// password toggle come back to this if i have time. formatting + spacing weird
document.addEventListener('DOMContentLoaded', function() {
    const togglePassword = document.getElementById('togglePassword');
    const password = document.getElementById('password');
    if (togglePassword && password) {
        togglePassword.addEventListener('click', function() {
            const type = password.type === 'password' ? 'text' : 'password';
            password.type = type;
            togglePassword.textContent = type === 'password' ? 'Show' : 'Hide';
        });
    }
});
// validation
window.validateStaffForm = function() {
    let isValid = true;
    const firstName = document.getElementById('first_name');
    const lastName = document.getElementById('last_name');
    const email = document.getElementById('email');
    const department = document.getElementById('department');
    const subject = document.getElementById('subject');
    const category = document.getElementById('category_id');
    const priority = document.getElementById('priority');
    const location = document.getElementById('location');
    const description = document.getElementById('description');
    clearError(firstName); clearError(lastName); clearError(email); clearError(department);
    clearError(subject); clearError(category); clearError(priority); clearError(location); clearError(description);
    if (firstName.value.trim().length < 2) {
        showError(firstName, 'First name must be at least 2 characters.'); isValid = false;
    }
    if (lastName.value.trim().length < 2) {
        showError(lastName, 'Last name must be at least 2 characters.'); isValid = false;
    }
    if (!validateEmail(email.value.trim())) {
        showError(email, 'Invalid email address.'); isValid = false;
    }
    if (!department.value) {
        showError(department, 'Please select a department.'); isValid = false;
    }
    if (subject.value.trim().length < 4) {
        showError(subject, 'Subject must be at least 4 characters.'); isValid = false;
    }
    if (!category.value) {
        showError(category, 'Please select a category.'); isValid = false;
    }
    if (!priority.value) {
        showError(priority, 'Please select a priority.'); isValid = false;
    }
    if (location.value.trim().length < 2) {
        showError(location, 'Location must be at least 2 characters.'); isValid = false;
    }
    if (description.value.trim().length < 10) {
        showError(description, 'Description must be at least 10 characters.'); isValid = false;
    }
    return isValid;
};
window.validateLoginForm = function() {
    let isValid = true;
    const username = document.getElementById('username');
    const password = document.getElementById('password');
    clearError(username); clearError(password);
    if (username.value.trim().length < 3) {
        showError(username, 'Username must be at least 3 characters long'); isValid = false;
    }
    if (password.value.length < 8) {
        showError(password, 'Password must be at least 8 characters long'); isValid = false;
    }
    return isValid;
}; 