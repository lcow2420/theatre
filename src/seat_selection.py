import tkinter as tk
from tkinter import messagebox
import random

class SeatSelection:
    def __init__(self, root, show, save_booking, old_seats=None):
        self.root = root
        self.show = show
        self.save_booking = save_booking
        self.old_seats = old_seats if old_seats else []

        self.seat_window = tk.Toplevel(root)
        self.seat_window.title(f"Select Seats for {show['title']}")
        self.seat_window.configure(bg='#f4f4f4')

        self.seat_frame = tk.Frame(self.seat_window, bg='#f4f4f4')
        self.seat_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.seat_grid = []
        self.booked_seats = self.get_booked_seats()
        self.current_selection = set()

        for i in range(10):  # 10 rows
            row = []
            for j in range(20):  # 20 columns
                seat = tk.Button(self.seat_frame, text=f"{i+1}-{j+1}", width=4, height=2, 
                                 bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                                 command=lambda r=i, c=j: self.select_seat(r, c))
                if (i, j) in self.booked_seats:
                    seat.config(bg='#e74c3c', state=tk.DISABLED)
                elif (i, j) in self.old_seats:
                    seat.config(bg='#f1c40f')
                seat.grid(row=i, column=j, padx=5, pady=5)
                row.append(seat)
            self.seat_grid.append(row)

        self.current_selection = set(self.old_seats)

        self.book_button = tk.Button(self.seat_window, text="Confirm", bg='#2ecc71', fg='white', font=('Arial', 12, 'bold'),
                                    command=self.confirm_seats, relief=tk.RAISED, bd=2)
        self.book_button.pack(pady=10)

    def get_booked_seats(self):
        # Fetch booked seats for the show
        booked_seats = set()
        # Example of adding some booked seats to the set
        booked_seats.update([(1, 1), (1, 2), (2, 1), (2, 2)])
        return booked_seats

    def select_seat(self, row, col):
        seat = self.seat_grid[row][col]
        if seat['bg'] == '#2ecc71':  # Green
            seat['bg'] = '#3498db'  # Original blue
            self.current_selection.discard((row, col))
        else:
            seat['bg'] = '#2ecc71'  # Green
            self.current_selection.add((row, col))

    def confirm_seats(self):
        if not self.current_selection:
            messagebox.showerror("Error", "Please select at least one seat.")
            return

        booking_ref = self.generate_booking_ref()
        old_seats = self.old_seats
        new_seats = list(self.current_selection)

        if old_seats:
            self.save_booking(self.show, old_seats, new_seats, booking_ref)
        else:
            self.save_booking(self.show, new_seats, booking_ref)  # Adjusted to match the number of arguments

        self.seat_window.destroy()

    def generate_booking_ref(self):
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
