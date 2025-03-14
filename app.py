from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_socketio import SocketIO, emit
from config import Config
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config.from_object(Config)

db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    license_plate = db.Column(db.String(20))
    lat = db.Column(db.Float, default=10.7918)
    lng = db.Column(db.Float, default=76.8276)
    speed = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='inactive')
    driver_name = db.Column(db.String(100))
    driver_contact = db.Column(db.String(20))
    driver_license = db.Column(db.String(50))
    driver_experience = db.Column(db.Integer)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid email or password"

    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    vehicles = Vehicle.query.all()
    return render_template('dashboard.html', vehicles=vehicles)

@app.route('/vehicle/<int:id>')
@login_required
def vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    return render_template('vehicle.html', vehicle=vehicle)

# NEW: Analytics page route
@app.route('/analytics')
@login_required
def analytics():
    return render_template('analytics.html')

# NEW: Geofences page route
@app.route('/geofences')
@login_required
def geofences():
    return render_template('geofences.html')

# SocketIO event for vehicle location updates
@socketio.on('location_update')
def handle_location(data):
    vehicle = Vehicle.query.get(data['id'])
    if vehicle:
        vehicle.lat = data['lat']
        vehicle.lng = data['lng']
        vehicle.speed = data['speed']
        if 'status' in data:
            vehicle.status = data['status']
        db.session.commit()
        emit('vehicle_update', {
            'id': vehicle.id,
            'lat': vehicle.lat,
            'lng': vehicle.lng,
            'speed': vehicle.speed,
            'status': vehicle.status
        }, broadcast=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app)

