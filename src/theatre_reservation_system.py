import tkinter as tk
from tkinter import messagebox
from ui_components import show_details
from seat_selection import SeatSelection
import sqlite3

class TheatreReservationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Theatre Reservation System")
        self.root.geometry("800x600")
        self.root.configure(bg='#ecf0f1')  # Set a light background color

        # Initialize database
        self.conn = sqlite3.connect('database/theatre.db')
        self.create_tables()

        # Setup GUI
        self.setup_gui()

    def create_tables(self):
        # Create tables if they don't exist
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                show_title TEXT NOT NULL,
                seats TEXT NOT NULL,
                booking_ref TEXT NOT NULL,
                user_id TEXT NOT NULL
            )
        ''')

    def setup_gui(self):
        # Main Frames
        self.main_frame = tk.Frame(self.root, bg='#ecf0f1')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(self.main_frame, bg='#34495e', width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.content_frame = tk.Frame(self.main_frame, bg='#ffffff')
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Sidebar buttons
        self.show_button = tk.Button(self.sidebar, text="Shows", command=self.load_shows, bg='#1abc9c', fg='white', font=('Arial', 12, 'bold'), relief=tk.FLAT)
        self.show_button.pack(fill=tk.X, pady=2, padx=10)

        self.bookings_button = tk.Button(self.sidebar, text="My Bookings", command=self.view_bookings, bg='#1abc9c', fg='white', font=('Arial', 12, 'bold'), relief=tk.FLAT)
        self.bookings_button.pack(fill=tk.X, pady=2, padx=10)

        # Content frame (dynamic based on selection)
        self.load_shows()

    def load_shows(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Load show data from the database
        shows = [
            {"title": "Harry Potter", "date": "2024-08-01", "time": "19:00", "theatre": "Main Hall"},
            {"title": "IT", "date": "2024-08-02", "time": "20:00", "theatre": "Second Hall"}
        ]

        # Display shows in a grid or list
        for show in shows:
            show_frame = tk.Frame(self.content_frame, bd=2, relief=tk.RAISED, bg='white', padx=10, pady=10)
            show_frame.pack(fill=tk.X, padx=10, pady=10)

            show_label = tk.Label(show_frame, text=f"{show['title']} - {show['date']} {show['time']}", font=('Arial', 14, 'bold'), bg='white')
            show_label.pack(side=tk.LEFT, padx=10)

            details_button = tk.Button(show_frame, text="Details", command=lambda s=show: show_details(self.root, s), bg='#3498db', fg='white', font=('Arial', 10, 'bold'), relief=tk.RAISED)
            details_button.pack(side=tk.RIGHT, padx=10)

            book_button = tk.Button(show_frame, text="Book Now", command=lambda s=show: self.select_seats(s), bg='#2ecc71', fg='white', font=('Arial', 10, 'bold'), relief=tk.RAISED)
            book_button.pack(side=tk.RIGHT, padx=10)

    def select_seats(self, show):
        # Display interactive seat selection
        SeatSelection(self.root, show, self.save_booking)

    def save_booking(self, show, selected_seats, booking_ref):
        seats_str = ','.join([f"{r+1}-{c+1}" for r, c in selected_seats])
        try:
            with self.conn:
                self.conn.execute('''
                    INSERT INTO bookings (show_title, seats, booking_ref, user_id)
                    VALUES (?, ?, ?, ?)
                ''', (show['title'], seats_str, booking_ref, 'user1'))  # Replace 'user1' with actual user ID
            print("Booking saved successfully.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def update_booking(self, show, old_seats, new_seats, booking_ref):
        seats_str = ','.join([f"{r+1}-{c+1}" for r, c in new_seats])
        try:
            with self.conn:
                # Remove old seats
                for seat in old_seats:
                    self.conn.execute('''
                        DELETE FROM bookings
                        WHERE show_title = ?
                          AND seats LIKE ?
                    ''', (show['title'], f"%{seat[0]+1}-{seat[1]+1}%"))

                # Insert new booking
                self.conn.execute('''
                    INSERT INTO bookings (show_title, seats, booking_ref, user_id)
                    VALUES (?, ?, ?, ?)
                ''', (show['title'], seats_str, booking_ref, 'user1'))  # Replace 'user1' with actual user ID

            print("Booking updated successfully.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def view_bookings(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Load bookings data from the database
        user_id = 'user1'  # Replace with actual user ID
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT show_title, seats, booking_ref
            FROM bookings
            WHERE user_id = ?
        ''', (user_id,))
        bookings = cursor.fetchall()

        # Display bookings in a list
        for booking in bookings:
            booking_frame = tk.Frame(self.content_frame, bd=2, relief=tk.RAISED, bg='white', padx=10, pady=10)
            booking_frame.pack(fill=tk.X, padx=10, pady=10)

            show_label = tk.Label(booking_frame, text=f"Show: {booking[0]}", font=('Arial', 12, 'bold'), bg='white')
            show_label.pack(side=tk.LEFT, padx=10)

            seats_label = tk.Label(booking_frame, text=f"Seats: {booking[1]}", font=('Arial', 12), bg='white')
            seats_label.pack(side=tk.LEFT, padx=10)

            modify_button = tk.Button(booking_frame, text="Modify", command=lambda b=booking: self.modify_booking(b), bg='#e67e22', fg='white', font=('Arial', 10, 'bold'), relief=tk.RAISED)
            modify_button.pack(side=tk.RIGHT, padx=10)

    def modify_booking(self, booking):
        # Display seat selection for modifying booking
        show = {"title": booking[0]}
        old_seats = [(int(seat.split('-')[0])-1, int(seat.split('-')[1])-1) for seat in booking[1].split(',')]
        SeatSelection(self.root, show, self.update_booking, old_seats)

if __name__ == "__main__":
    root = tk.Tk()
    app = TheatreReservationSystem(root)
    root.mainloop()
