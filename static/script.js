// Set today's date as default for date input
document.addEventListener('DOMContentLoaded', function() {
    const dateInput = document.getElementById('date_applied');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.value = today;
    }
});

// Auto-hide flash messages after 5 seconds
const alerts = document.querySelectorAll('.alert');
alerts.forEach(alert => {
    setTimeout(() => {
        alert.style.opacity = '0';
        alert.style.transition = 'opacity 0.5s';
        setTimeout(() => alert.remove(), 500);
    }, 5000);
});
