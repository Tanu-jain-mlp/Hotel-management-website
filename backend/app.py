from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Path to project root (one level above backend)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# ==========================
# DATABASE SETUP
# ==========================

def init_db():
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        room_type TEXT NOT NULL,
        check_in TEXT NOT NULL,
        check_out TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ==========================
# FRONTEND ROUTES
# ==========================

@app.route('/')
def home():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/asset/<path:filename>')
def assets(filename):
    return send_from_directory(
        os.path.join(BASE_DIR, 'asset'),
        filename
    )

@app.route('/<path:filename>')
def html_pages(filename):
    return send_from_directory(BASE_DIR, filename)

# ==========================
# BOOKING API
# ==========================

@app.route('/book', methods=['POST'])
def book_room():
    data = request.json

    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    room_type = data.get('room_type')
    check_in = data.get('check_in')
    check_out = data.get('check_out')

    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO bookings
        (name, email, phone, room_type, check_in, check_out)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        phone,
        room_type,
        check_in,
        check_out
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Booking Successful!"
    })

@app.route('/bookings', methods=['GET'])
def get_bookings():

    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM bookings
    """)

    bookings = cursor.fetchall()

    conn.close()

    return jsonify(bookings)

# ==========================
# RUN APP
# ==========================

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
