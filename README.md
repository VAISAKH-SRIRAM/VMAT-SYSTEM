# VMAT System (Vehicle Management & Tracking System)

## Overview

VMAT System is a web application designed for real-time vehicle management and tracking. It features live GPS tracking, dynamic data updates, and interactive analytics with a modern, responsive UI. The app integrates key functionalities such as geofence management and a built-in dark/light theme toggle, ensuring an optimal user experience across all devices.

## Features

- **Real-Time Vehicle Tracking:**  
  Display live vehicle locations, speeds, and statuses on an interactive map using Leaflet and Socket.IO.

- **Dashboard:**  
  View real-time updates and vehicle details, ensuring you always have current information at your fingertips.

- **Analytics:**  
  Interactive charts powered by Chart.js visualize metrics like speed distribution and geofence activity.

- **Geofence Management:**  
  Manage and monitor geofences through a dedicated interface.

- **Theme Toggle:**  
  Easily switch between dark and light themes with a toggle button, ensuring your interface suits your preference and environment.

- **Responsive Design:**  
  The UI is fully responsive, providing an excellent experience on desktops, tablets, and mobile devices.

## Technology Stack

- **Backend:**  
  Flask, Flask-SocketIO, Flask-Login, Flask-SQLAlchemy, Flask-Migrate

- **Frontend:**  
  HTML, CSS (with glassmorphism and neuomorphic styling), JavaScript, Chart.js, Leaflet, Font Awesome

- **Real-Time Communication:**  
  Socket.IO

- **Database:**  
  SQLAlchemy (compatible with SQLite, PostgreSQL, MySQL, etc.)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/VMAT-System.git
   cd VMAT-System
