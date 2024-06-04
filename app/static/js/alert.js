setTimeout(() => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        new bootstrap.Alert(alert).close();
    });
}, 5000);