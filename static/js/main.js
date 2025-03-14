document.addEventListener('DOMContentLoaded', () => {
  // Smooth fade-in effect on load
  document.body.classList.remove('fade-out');

  // Initialize Socket.IO for real-time communication
  const socket = io();

  // Smooth page transition for internal links
  document.querySelectorAll('a').forEach(link => {
    if (link.host === window.location.host) {
      link.addEventListener('click', e => {
        e.preventDefault();
        document.body.classList.add('fade-out');
        setTimeout(() => window.location = link.href, 300);
      });
    }
  });

  // Listen for vehicle updates
  socket.on('vehicle_update', data => {
    const vehicleElement = document.querySelector(`[data-vehicle-id="${data.id}"]`);
    if (vehicleElement) {
      const speedElement = vehicleElement.querySelector('.vehicle-speed');
      if (speedElement) {
        speedElement.textContent = `${data.speed} km/h`;
      }
      const statusElement = vehicleElement.querySelector('.vehicle-status');
      if (statusElement) {
        statusElement.className = `vehicle-status status-${data.status}`;
      }
    }
  });

  // Listen for alerts and display using showAlert
  socket.on('alert', data => {
    showAlert(data.message);
  });

  // Handle socket connection errors
  socket.on('connect_error', () => {
    showAlert('Connection lost. Trying to reconnect...', 'error');
  });
});

/**
 * Display alert toast messages.
 * @param {string} message - The alert message.
 * @param {string} type - Alert type (default 'info').
 */
function showAlert(message, type = 'info') {
  const alertDiv = document.createElement('div');
  alertDiv.className = `alert-toast alert-${type}`;
  alertDiv.innerHTML = `
    <div class="alert-content">
      <i class="fas fa-bell"></i>
      <span>${message}</span>
    </div>
  `;
  document.body.appendChild(alertDiv);
  setTimeout(() => {
    alertDiv.classList.add('hide');
    setTimeout(() => alertDiv.remove(), 300);
  }, 3000);
}

