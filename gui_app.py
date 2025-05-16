import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from book_library import Book, EBook, Library, BookNotAvailableError

# Create an instance of Library to manage our books
library = Library()

# Initialize the main window for the GUI
root = tk.Tk()
root.title("Library Management System")
root.geometry("700x700")  # Set a larger window size
root.resizable(False, False)  # Prevent resizing for consistent layout

# Configure style
style = ttk.Style()
style.configure('TFrame', background='#f0f0f0')
style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
style.configure('TButton', font=('Arial', 10))
style.configure('TEntry', font=('Arial', 10))
style.configure('TCheckbutton', background='#f0f0f0', font=('Arial', 10))

# ====================== Main Frames ======================
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

# Left frame for book input
input_frame = ttk.LabelFrame(main_frame, text="Add New Book", padding="10")
input_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

# Right frame for book management
action_frame = ttk.LabelFrame(main_frame, text="Book Actions", padding="10")
action_frame.grid(row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)

# Bottom frame for book list
list_frame = ttk.LabelFrame(main_frame, text="Library Inventory", padding="10")
list_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)

# Configure grid weights
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(1, weight=1)

# ====================== Function Definitions ======================
def toggle_ebook_fields():
    """Enable/disable eBook fields based on checkbox state"""
    if ebook_var.get():
        size_entry.config(state=tk.NORMAL)
        size_entry.delete(0, tk.END)
    else:
        size_entry.config(state=tk.DISABLED)
        size_entry.delete(0, tk.END)

def validate_size_input(new_val):
    """Validate that download size is a positive number"""
    if not new_val:  # Allow empty field
        return True
    try:
        float(new_val)
        return float(new_val) > 0
    except ValueError:
        return False

def add_book():
    """Adds a new book or eBook to the library with validation"""
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    isbn = isbn_entry.get().strip()
    is_ebook = ebook_var.get()
    size = size_entry.get().strip() if is_ebook else None

    # Basic validation
    if not title or not author or not isbn:
        messagebox.showerror("Error", "Title, Author, and ISBN are required.")
        return

    if is_ebook:
        if not size:
            messagebox.showerror("Error", "Download size required for eBooks.")
            return
        try:
            size = float(size)
            if size <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Download size must be a positive number.")
            return

    # Create the appropriate book object
    try:
        if is_ebook:
            book = EBook(title, author, isbn, size)
        else:
            book = Book(title, author, isbn)

        library.add_book(book)
        messagebox.showinfo("Success", f"Book '{title}' added to the library.")
        clear_input_fields()
        update_book_list()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add book: {str(e)}")

def clear_input_fields():
    """Clear all input fields"""
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    isbn_entry.delete(0, tk.END)
    ebook_var.set(False)
    size_entry.delete(0, tk.END)
    toggle_ebook_fields()

def lend_book():
    """Lends a book by ISBN with validation"""
    isbn = simpledialog.askstring("Lend Book", "Enter ISBN of the book to lend:").strip()
    if not isbn:
        return
        
    try:
        library.lend_book(isbn)
        messagebox.showinfo("Success", "Book lent successfully.")
        update_book_list()
    except BookNotAvailableError as e:
        messagebox.showerror("Error", str(e))

def return_book():
    """Returns a book by ISBN with validation"""
    isbn = simpledialog.askstring("Return Book", "Enter ISBN of the book to return:").strip()
    if not isbn:
        return
        
    try:
        library.return_book(isbn)
        messagebox.showinfo("Success", "Book returned successfully.")
        update_book_list()
    except BookNotAvailableError as e:
        messagebox.showerror("Error", str(e))

def remove_book():
    """Removes a book from the library by ISBN with validation"""
    isbn = simpledialog.askstring("Remove Book", "Enter ISBN of the book to remove:").strip()
    if not isbn:
        return
        
    library.remove_book(isbn)
    messagebox.showinfo("Success", "Book removed from library.")
    update_book_list()

def view_books_by_author():
    """Displays books by a specific author"""
    author = simpledialog.askstring("Search by Author", "Enter author's name:").strip()
    if not author:
        return
        
    books = list(library.books_by_author(author))
    if books:
        listbox.delete(0, tk.END)
        listbox.insert(tk.END, f"Books by {author}:")
        for book in books:
            listbox.insert(tk.END, str(book))
    else:
        messagebox.showinfo("Not Found", "No books by this author.")

def update_book_list():
    """Updates the Listbox with available books"""
    listbox.delete(0, tk.END)
    listbox.insert(tk.END, "Available Books:")
    for book in library:
        listbox.insert(tk.END, str(book))

# ====================== Input Frame Widgets ======================
# Title
ttk.Label(input_frame, text="Title:").grid(row=0, column=0, sticky=tk.W, pady=2)
title_entry = ttk.Entry(input_frame, width=30)
title_entry.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)

# Author
ttk.Label(input_frame, text="Author:").grid(row=1, column=0, sticky=tk.W, pady=2)
author_entry = ttk.Entry(input_frame, width=30)
author_entry.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)

# ISBN
ttk.Label(input_frame, text="ISBN:").grid(row=2, column=0, sticky=tk.W, pady=2)
isbn_entry = ttk.Entry(input_frame, width=30)
isbn_entry.grid(row=2, column=1, padx=5, pady=2, sticky=tk.W)

# eBook checkbox
ebook_var = tk.BooleanVar()
ebook_cb = ttk.Checkbutton(
    input_frame, 
    text="eBook?", 
    variable=ebook_var,
    command=toggle_ebook_fields
)
ebook_cb.grid(row=3, column=0, columnspan=2, pady=5, sticky=tk.W)

# Download size (only for eBooks)
ttk.Label(input_frame, text="Download Size (MB):").grid(row=4, column=0, sticky=tk.W, pady=2)
size_entry = ttk.Entry(input_frame, width=30, state=tk.DISABLED)
size_entry.grid(row=4, column=1, padx=5, pady=2, sticky=tk.W)

# Register validation for size entry
validate_size = root.register(validate_size_input)
size_entry.config(validate="key", validatecommand=(validate_size, '%P'))

# Add book button
add_btn = ttk.Button(input_frame, text="Add Book", command=add_book)
add_btn.grid(row=5, column=0, columnspan=2, pady=10)

# Clear fields button
clear_btn = ttk.Button(input_frame, text="Clear Fields", command=clear_input_fields)
clear_btn.grid(row=6, column=0, columnspan=2, pady=5)

# ====================== Action Frame Widgets ======================
# Lend book button
lend_btn = ttk.Button(action_frame, text="Lend Book", command=lend_book)
lend_btn.pack(fill=tk.X, pady=5)

# Return book button
return_btn = ttk.Button(action_frame, text="Return Book", command=return_book)
return_btn.pack(fill=tk.X, pady=5)

# Remove book button
remove_btn = ttk.Button(action_frame, text="Remove Book", command=remove_book)
remove_btn.pack(fill=tk.X, pady=5)

# View books by author button
author_btn = ttk.Button(action_frame, text="View Books by Author", command=view_books_by_author)
author_btn.pack(fill=tk.X, pady=5)

# ====================== List Frame Widgets ======================
# Listbox with scrollbar
scrollbar = ttk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(
    list_frame, 
    width=80, 
    height=15, 
    yscrollcommand=scrollbar.set,
    font=('Courier New', 10)
)
listbox.pack(fill=tk.BOTH, expand=True)

scrollbar.config(command=listbox.yview)

# Status bar
status_bar = ttk.Label(
    root, 
    text="Ready", 
    relief=tk.SUNKEN, 
    anchor=tk.W,
    font=('Arial', 9)
)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Initialize the book list
update_book_list()

# Start the GUI event loop
root.mainloop()