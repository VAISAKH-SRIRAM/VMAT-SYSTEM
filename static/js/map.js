// Initialize the map with a default center and zoom level
const map = L.map('map').setView([10.7918, 76.8276], 13);

// Store markers by vehicle ID
const markers = new Map();

// Initialize Socket.IO for real-time updates
const socket = io();

// Add OpenStreetMap tile layer
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Add scale control to the bottom left
L.control.scale({ position: 'bottomleft' }).addTo(map);

// Add fullscreen control if available
if (L.Control.Fullscreen) {
  map.addControl(new L.Control.Fullscreen());
}

// Listen for vehicle updates
socket.on('vehicle_update', data => {
  const iconHtml = `
    <div class="marker-pin">
      <i class="fas ${data.speed > 0 ? 'fa-truck-moving' : 'fa-truck-pickup'}"></i>
    </div>
  `;
  const vehicleIcon = L.divIcon({
    className: 'vehicle-marker',
    html: iconHtml,
    iconSize: [40, 40]
  });

  if (markers.has(data.id)) {
    const marker = markers.get(data.id);
    marker.setLatLng([data.lat, data.lng]);
    marker.setIcon(vehicleIcon);
  } else {
    const marker = L.marker([data.lat, data.lng], { icon: vehicleIcon }).addTo(map);
    markers.set(data.id, marker);
  }
});

// Re-render map on window resize
window.addEventListener('resize', () => {
  map.invalidateSize();
});

