import sqlite3

def create_tables(conn):
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                show_title TEXT NOT NULL,
                seats TEXT NOT NULL,
                booking_ref TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS reserved_seats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                show_title TEXT NOT NULL,
                seat TEXT NOT NULL
            )
        ''')

def save_booking(conn, show, selected_seats, booking_ref):
    seats_str = ','.join([f"{r+1}-{c+1}" for r, c in selected_seats])
    try:
        with conn:
            conn.execute('''
                INSERT INTO bookings (show_title, seats, booking_ref)
                VALUES (?, ?, ?)
            ''', (show['title'], seats_str, booking_ref))
            for seat in selected_seats:
                conn.execute('''
                    INSERT INTO reserved_seats (show_title, seat)
                    VALUES (?, ?)
                ''', (show['title'], f"{seat[0]+1}-{seat[1]+1}"))
    except sqlite3.Error as e:
        print(f"Database error: {e}")
