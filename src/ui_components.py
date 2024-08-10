import tkinter as tk

def show_details(root, show):
    """ Display details of a show in a new window. """
    details_window = tk.Toplevel(root)
    details_window.title(f"{show['title']} - Details")

    details_frame = tk.Frame(details_window, padx=10, pady=10, bg='white')
    details_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    details_text = (
        f"Title: {show['title']}\n"
        f"Date: {show['date']}\n"
        f"Time: {show['time']}\n"
        f"Theatre: {show['theatre']}"
    )
    label = tk.Label(details_frame, text=details_text, font=('Arial', 12), bg='white')
    label.pack(padx=10, pady=10)

    close_button = tk.Button(details_frame, text="Close", command=details_window.destroy)
    close_button.pack(pady=10)

    details_window.update_idletasks()
    window_width = details_window.winfo_width()
    window_height = details_window.winfo_height()
    screen_width = details_window.winfo_screenwidth()
    screen_height = details_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    details_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
