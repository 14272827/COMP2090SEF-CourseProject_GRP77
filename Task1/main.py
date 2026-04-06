import tkinter as tk
from tkinter import messagebox, simpledialog
from library import Library
from book import Book
from user import User

lib = Library()

# Pre‑add some sample books for testing
Book("Clean Code", "Robert C. Martin", "9780132350884")
Book("Python Crash Course", "Eric Matthes", "9781593279288")
Book("Design Patterns", "Erich Gamma", "9780201633610")
# Add a second copy of Clean Code
Book("Clean Code", "Robert C. Martin", "9780132350884")

def create_window():
    window = tk.Tk()
    window.geometry("500x500")
    window.title("Library Management System")
    return window

def show_choice_frame(parent):
    tk.Label(parent, text="Library Management System", font=("Arial", 20)).pack()
    tk.Button(parent, text="Register", command=lambda: register_window(), width = 20, height = 3, font=("Arial", 20)).pack()
    tk.Button(parent, text="Login", command=lambda: login_window(),  width = 20, height = 3, font=("Arial", 20)).pack()
    tk.Button(parent, text="Search book", command = search_book,  width = 20, height = 3, font=("Arial", 20)).pack()

def register_window():
    win = tk.Toplevel()
    win.title("Register")
    win.geometry("400x500")
    tk.Frame(win, height = 50).pack()

    tk.Label(win, text="Username", font=("Arial", 25)).pack()
    uid_entry = tk.Entry(win, font=("Arial", 20), width=15)
    uid_entry.pack()

    tk.Label(win, text="Password", font=("Arial", 25)).pack()
    pw_entry = tk.Entry(win, show="*", font=("Arial", 20), width=15)
    pw_entry.pack()

    tk.Label(win, text="Role (user/admin)", font=("Arial", 25)).pack()
    role_entry = tk.Entry(win, font=("Arial", 20), width=15)
    role_entry.pack()

    tk.Label(win, text="Admin code (if admin)", font=("Arial", 25)).pack()
    code_entry = tk.Entry(win, font=("Arial", 20), width=15)
    code_entry.pack()

    def do_register():
        uid, pw, role, code = uid_entry.get(), pw_entry.get(), role_entry.get(), code_entry.get()

        if not uid or not pw or not role:
            messagebox.showerror("Error", "Please fill all fields.")
            return
        if role.lower() not in ["user", "admin"]:
            messagebox.showerror("Error", "Role must be user or admin")
            return
        if role.lower() == "admin" and not code:
            messagebox.showerror("Error", "Admin code required")
            return

        success, msg = lib.register_user(uid, pw, role, code)
        if success:
            messagebox.showinfo("Success", msg)
            win.destroy()
        else:
            messagebox.showerror("Error", msg)

    tk.Button(win, text="Register", command=do_register, width=15, height=2, font=("Arial", 20)).pack(pady=20)

def login_window():
    win = tk.Toplevel()
    win.title("Login")
    win.geometry("400x500")
    tk.Frame(win, height=50).pack()

    tk.Label(win, text="Username",font=("Arial", 25)).pack()
    uid_entry = tk.Entry(win, font=("Arial", 20), width=15)
    uid_entry.pack()

    tk.Label(win, text="Password",font=("Arial", 25)).pack()
    pw_entry = tk.Entry(win, show="*", font=("Arial", 20), width=15)
    pw_entry.pack()

    def do_login():
        uid, pw = uid_entry.get(), pw_entry.get()

        if not uid or not pw:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        success, msg = lib.login(uid, pw)
        if success:
            messagebox.showinfo("Success", msg)
            win.destroy()
            menu_window()
        else:
            messagebox.showerror("Error", msg)

    tk.Button(win, text="Login", command = do_login, width=15, height=2, font=("Arial", 20)).pack()

def search_book():
    keyword = simpledialog.askstring("Search Book", "Enter title/author/ISBN: ")
    if keyword:
        results = lib.search_book(keyword)
        if not results:
            messagebox.showerror("Search Results", "No corresponding books found")
        else:
            display_text = "Search results:\n\n"
            for book in results:
                display_text = display_text + str(book) + "\n\n"
            messagebox.showinfo("Search Results", display_text)

def borrow_book():
    username = lib.current_user.get_username()
    ISBN = simpledialog.askstring("Borrow Book", "Enter ISBN of the book to borrow:")
    if not ISBN:
        return

    success, message = lib.borrow_book(username, ISBN)
    if success:
        messagebox.showinfo("Success", message)
    else:
        messagebox.showerror("Error", message)

def return_book():
    records = lib.current_user.get_borrow_records()
    if not records:
        messagebox.showinfo("Info", "You have no borrowed books.")
        return

    return_text = "Please input the Book ID you want to return:\n\n"
    for book_id in records:
        book = Book.get_book_by_id(book_id)
        return_text = return_text + str(book_id) + ". " + book.get_title() + "\n"

    book_id_str = simpledialog.askstring("Return Book", return_text)
    if not book_id_str:
        return

    try:
        book_id = int(book_id_str)
        if book_id not in records:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Invalid Book ID.")
        return

    success, message = lib.return_book(lib.current_user.get_username(), book_id)
    if success:
        messagebox.showinfo("Success", message)
    else:
        messagebox.showerror("Error", message)

def view_borrow_records():
    success, result = lib.view_borrow_records()
    if not success:
        messagebox.showerror("Error", result)
    else:
        if not result:
            messagebox.showinfo("Borrow Records", "No borrow records.")
        else:
            display_text = "Your borrowed books:\n\n"
            for line in result:
                display_text = display_text + line + "\n\n"
            messagebox.showinfo("Borrow Records", display_text)

def change_password_admin():
    target = simpledialog.askstring("Change Password", "Enter username to change password:")
    if not target:
        return

    if not User.exists(target):
        messagebox.showerror("Error", "Username not found.")
        return

    old_pw = simpledialog.askstring("Change Password", "Enter current password of that user:")
    if not old_pw:
        return

    new_pw = simpledialog.askstring("Change Password", "Enter new password:")
    if not new_pw:
        return

    success, message = lib.change_password(old_pw, new_pw, username=target)
    if success:
        messagebox.showinfo("Success", message)
    else:
        messagebox.showerror("Error", message)

def change_username_admin():
    old_username = simpledialog.askstring("Change Username", "Enter current username:")
    if not old_username:
        return

    if not User.exists(old_username):
        messagebox.showerror("Error", "Username not found.")
        return

    new_username = simpledialog.askstring("Change Username", "Enter new username:")
    if not new_username:
        return

    if User.exists(new_username):
        messagebox.showerror("Error", "New username is already taken.")
        return

    success, message = lib.change_username(old_username, new_username)
    if success:
        messagebox.showinfo("Success", message)
    else:
        messagebox.showerror("Error", message)

def view_any_records():
    username = simpledialog.askstring("View Records", "Enter username to view borrow records:")
    if not username:
        return

    if not User.exists(username):
        messagebox.showerror("Error", "Username not found.")
        return

    success, result = lib.view_borrow_records(username)
    if not success:
        if result == "No borrow records.":
            messagebox.showinfo("Borrow Records", "No borrow records for " + username)
        else:
            messagebox.showerror("Error", result)
    else:
        if not result:
            messagebox.showinfo("Borrow Records", "No borrow records for " + username)
        else:
            display_text = "Borrow records for " + username + ":\n\n"
            for line in result:
                display_text = display_text + line + "\n\n"
            messagebox.showinfo("Borrow Records", display_text)

def logout():
    success, msg = lib.logout()
    if success:
        messagebox.showinfo("Logout", msg)
        window = tk._default_root
        for widget in window.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()
    else:
        messagebox.showerror("Error", msg)

def change_own_pw():
    old_pw = simpledialog.askstring("Change Password", "Enter current password:")
    if not old_pw:
        messagebox.showerror("Error", "Please enter the current password.")
        return
    new_pw = simpledialog.askstring("Change Password", "Enter new password:")
    if not new_pw:
        messagebox.showerror("Error", "Please enter a new password.")
        return
    success, message = lib.change_password(old_pw, new_pw)
    if success:
        messagebox.showinfo("Success", message)
    else:
        messagebox.showerror("Error", message)

def menu_window():
    window = tk.Toplevel()
    window.geometry("600x600")
    window.title("Menu")

    tk.Label(window, text="Welcome " + lib.current_user.get_username(), width=25, height=2, font=("Arial", 20)).pack()

    tk.Button(window, text="Search book", command = search_book, width = 20, height = 3, font=("Arial", 20)).pack()
    tk.Button(window, text="Borrow a book", command = borrow_book, width = 20, height = 3, font=("Arial", 20)).pack()
    tk.Button(window, text="Return book", command = return_book, width = 20, height = 3, font=("Arial", 20)).pack()
    tk.Button(window, text="Change password", command = change_own_pw, width = 20, height = 3, font=("Arial", 20)).pack()

    if lib.current_user.has_permission():
        tk.Button(window, text="Change another user's password", command = change_password_admin, width = 20, height = 3, font=("Arial", 20)).pack()
        tk.Button(window, text="View any user's borrow records", command = view_any_records, width = 20, height = 3, font=("Arial", 20)).pack()

    tk.Button(window, text = "Logout", command = logout, width = 20, height = 3, font=("Arial", 20)).pack()

if __name__ == "__main__":
    root = create_window()
    show_choice_frame(root)
    root.mainloop()
