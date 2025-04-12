document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById('registrationForm');
    if (!form) return;

    form.addEventListener('input', function () {
        validateForm();
    });

    function validateForm() {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        const submitBtn = document.getElementById('submitBtn');
        const errorElement = document.getElementById('passwordError');

        let isValid = true;

        if (!username || !password || !confirmPassword) {
            isValid = false;
        }
        if (password.length < 8) {
            errorElement.textContent = 'Password must be at least 8 characters long';
            errorElement.classList.remove('success');
            errorElement.classList.add('error');
            isValid = false;
        } else if (password !== confirmPassword) {
            errorElement.textContent = 'Passwords do not match';
            errorElement.classList.remove('success');
            errorElement.classList.add('error');
            isValid = false;
        } else {
            errorElement.textContent = 'Passwords match';
            errorElement.classList.remove('error');
            errorElement.classList.add('success');
        }

        submitBtn.disabled = !isValid;
        submitBtn.classList.toggle('enabled', isValid);
    }
});
