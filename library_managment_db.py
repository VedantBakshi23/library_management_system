import tkinter as tk
from tkinter import messagebox
import sqlite3

class LibraryManagement:
    def __init__(self, master):
        self.master = master
        self.master.title("Library Management System")
        self.master.geometry("500x600")
        self.master.config(bg='#708090')

        # Connect to SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect("library.db")
        self.cursor = self.conn.cursor()

        # Initialize the database
        self.initialize_db()

        # Labels for login
        self.login_label = tk.Label(self.master, text="Library Management System", font=("Helvetica", 16), bg='#708090', fg='white')
        self.login_label.pack(pady=10)
        self.username_label = tk.Label(self.master, text="Username", font=("Helvetica", 12), bg='#708090', fg='white')
        self.username_label.pack()
        self.username_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.username_entry.pack()
        self.password_label = tk.Label(self.master, text="Password", font=("Helvetica", 12), bg='#708090', fg='white')
        self.password_label.pack()
        self.password_entry = tk.Entry(self.master, font=("Helvetica", 12), show="*")
        self.password_entry.pack()

        # Buttons for login and registration
        self.login_button = tk.Button(self.master, text="Login", command=self.login, font=("Helvetica", 12))
        self.login_button.pack(pady=5)
        self.register_button = tk.Button(self.master, text="Register", command=self.register, font=("Helvetica", 12))
        self.register_button.pack(pady=5)

        # Button for reset system
        self.reset_button = tk.Button(self.master, text="Reset System", command=self.reset_system, font=("Helvetica", 12), bg='red', fg='white')
        self.reset_button.pack(pady=5)

    def initialize_db(self):
        # Create tables for librarians and books
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS librarians (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                isbn TEXT,
                year TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS issued_books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                FOREIGN KEY(book_id) REFERENCES books(id)
            )
        """)
        self.conn.commit()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.cursor.execute("SELECT * FROM librarians WHERE username = ? AND password = ?", (username, password))
        librarian = self.cursor.fetchone()
        if librarian:
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.login_label.destroy()
            self.username_label.destroy()
            self.username_entry.destroy()
            self.password_label.destroy()
            self.password_entry.destroy()
            self.login_button.destroy()
            self.register_button.destroy()
            self.reset_button.destroy()
            self.library_management_screen(librarian[3])  # Pass role (admin/user)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            self.cursor.execute("INSERT INTO librarians (username, password, role) VALUES (?, ?, ?)", (username, password, "user"))
            self.conn.commit()
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Registration successful")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

    def reset_system(self):
        # Clear all data in the database
        if messagebox.askyesno("Reset System", "Are you sure you want to reset the entire system? This action cannot be undone."):
            self.cursor.execute("DELETE FROM librarians")
            self.cursor.execute("DELETE FROM books")
            self.cursor.execute("DELETE FROM issued_books")
            self.conn.commit()
            messagebox.showinfo("Success", "System reset successfully.")

    def library_management_screen(self, role):
        # Add Book Section
        self.book_title_label = tk.Label(self.master, text="Book Title", font=("Helvetica", 12), bg='#708090', fg='white')
        self.book_title_label.pack()
        self.book_title_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.book_title_entry.pack()

        self.book_author_label = tk.Label(self.master, text="Author", font=("Helvetica", 12), bg='#708090', fg='white')
        self.book_author_label.pack()
        self.book_author_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.book_author_entry.pack()

        self.book_isbn_label = tk.Label(self.master, text="ISBN", font=("Helvetica", 12), bg='#708090', fg='white')
        self.book_isbn_label.pack()
        self.book_isbn_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.book_isbn_entry.pack()

        self.book_year_label = tk.Label(self.master, text="Year", font=("Helvetica", 12), bg='#708090', fg='white')
        self.book_year_label.pack()
        self.book_year_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.book_year_entry.pack()

        self.add_book_button = tk.Button(self.master, text="Add Book", command=self.add_book, font=("Helvetica", 12))
        self.add_book_button.pack(pady=5)

        # View Books Button
        self.view_books_button = tk.Button(self.master, text="View Books", command=self.view_books, font=("Helvetica", 12))
        self.view_books_button.pack(pady=5)

        # Remove Book Section
        self.remove_book_label = tk.Label(self.master, text="Remove Book by Title", font=("Helvetica", 12), bg='#708090', fg='white')
        self.remove_book_label.pack()
        self.remove_book_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.remove_book_entry.pack()
        self.remove_book_button = tk.Button(self.master, text="Remove Book", command=self.remove_book, font=("Helvetica", 12))
        self.remove_book_button.pack(pady=5)

    def add_book(self):
        title = self.book_title_entry.get()
        author = self.book_author_entry.get()
        isbn = self.book_isbn_entry.get()
        year = self.book_year_entry.get()

        self.cursor.execute("INSERT INTO books (title, author, isbn, year) VALUES (?, ?, ?, ?)", (title, author, isbn, year))
        self.conn.commit()
        messagebox.showinfo("Success", "Book added successfully")
        self.book_title_entry.delete(0, tk.END)
        self.book_author_entry.delete(0, tk.END)
        self.book_isbn_entry.delete(0, tk.END)
        self.book_year_entry.delete(0, tk.END)

    def remove_book(self):
        title = self.remove_book_entry.get()
        self.cursor.execute("DELETE FROM books WHERE title = ?", (title,))
        self.conn.commit()
        messagebox.showinfo("Success", "Book removed successfully")
        self.remove_book_entry.delete(0, tk.END)

    def view_books(self):
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()
        if books:
            book_list = "\n".join([f"Title: {book[1]}, Author: {book[2]}, ISBN: {book[3]}, Year: {book[4]}" for book in books])
        else:
            book_list = "No books available."
        messagebox.showinfo("Books", book_list)

    def __del__(self):
        # Close the database connection when the program terminates
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagement(root)
    root.mainloop()
