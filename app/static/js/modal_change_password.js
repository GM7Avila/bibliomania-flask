// submit ao evento de click do button change-password-form
document.addEventListener("DOMContentLoaded", function() {
    const confirmPasswordButton = document.getElementById('confirm-password');
    const changePasswordForm = document.getElementById('change-password-form');

    confirmPasswordButton.addEventListener('click', function() {
        changePasswordForm.submit();
    });
});