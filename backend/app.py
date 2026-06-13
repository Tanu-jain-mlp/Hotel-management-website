from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)

CORS(app)

# NEW ROUTE
@app.route('/')
def home():
    return "Hotel Management Backend Running Successfully"


@app.route('/book', methods=['POST'])
def book_room():

    data = request.json

    city = data['city']
    rooms = data['rooms']
    adults = data['adults']
    children = data['children']
    checkin = data['checkin']
    checkout = data['checkout']

    conn = sqlite3.connect("hotel.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO bookings
    (city, rooms, adults, children, checkin, checkout)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
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
        "message": "Booking Successful"
    })


@app.route('/bookings', methods=['GET'])
def get_bookings():

    conn = sqlite3.connect("hotel.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings")

    rows = cursor.fetchall()

    conn.close()

    bookings = []

    for row in rows:
        bookings.append({
            "id": row[0],
            "city": row[1],
            "rooms": row[2],
            "adults": row[3],
            "children": row[4],
            "checkin": row[5],
            "checkout": row[6]
        })

    return jsonify(bookings)


if __name__ == '__main__':
    app.run(debug=True)
