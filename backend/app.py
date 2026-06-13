from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Project root directory
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
        city TEXT,
        rooms INTEGER,
        adults INTEGER,
        children INTEGER,
        checkin TEXT,
        checkout TEXT
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
def pages(filename):
    return send_from_directory(BASE_DIR, filename)

# ==========================
# BOOKING API
# ==========================

@app.route('/book', methods=['POST'])
def book_room():

    data = request.get_json()

    city = data.get('city')
    rooms = data.get('rooms')
    adults = data.get('adults')
    children = data.get('children')
    checkin = data.get('checkin')
    checkout = data.get('checkout')

    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO bookings
    (city, rooms, adults, children, checkin, checkout)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        city,
        rooms,
        adults,
        children,
        checkin,
        checkout
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
