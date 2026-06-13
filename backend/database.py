import sqlite3

def create_database():

    conn = sqlite3.connect("hotel.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings(
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

if __name__ == "__main__":
    create_database()
