import tkinter as tk
from tkinter import messagebox, simpledialog
from library import Library
from book import Book
from user import User

# create a instance of library
lib = Library()

# Pre‑add some sample books for testing
Book("Clean Code", "Robert C. Martin", "9780132350884")
Book("Python Crash Course", "Eric Matthes", "9781593279288")
Book("Design Patterns", "Erich Gamma", "9780201633610")
# Add a second copy of Clean Code
Book("Clean Code", "Robert C. Martin", "9780132350884")

# create the main application window
def create_window():
    window = tk.Tk()
    window.geometry("500x500")
    window.title("Library Management System")
    return window

# display the main menu with Register, Login and Search Book function
def show_choice_frame(parent):
    tk.Label(parent, text="Library Management System", font=("Arial", 20)).pack()
    tk.Button(parent, text="Register", command=lambda: register_window(), width = 20, height = 3, font=("Arial", 20)).pack()
    tk.Button(parent, text="Login", command=lambda: login_window(),  width = 20, height = 3, font=("Arial", 20)).pack()
    tk.Button(parent, text="Search book", command = search_book,  width = 20, height = 3, font=("Arial", 20)).pack()

# create the registration window
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

    # perform registration: get input and call Library.register_user
    def do_register():
        # get information from user by input
        uid, pw, role, code = uid_entry.get(), pw_entry.get(), role_entry.get(), code_entry.get()

        # verify all fields are filled
        if not uid or not pw or not role:
            messagebox.showerror("Error", "Please fill all fields.")
            return
        # check if role is user or admin
        if role.lower() not in ["user", "admin"]:
            messagebox.showerror("Error", "Role must be user or admin")
            return
        # check if user select admin but no admin code, reject registration
        if role.lower() == "admin" and not code:
            messagebox.showerror("Error", "Admin code required")
            return
        # call Library's method to reigister a new user
        success, msg = lib.register_user(uid, pw, role, code)
        if success:
            messagebox.showinfo("Success", msg)
            win.destroy() # close registration window
        else:
            messagebox.showerror("Error", msg)

    tk.Button(win, text="Register", command=do_register, width=15, height=2, font=("Arial", 20)).pack(pady=20)

# create the login window
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

    # perform login: get input and call Library.login
    def do_login():
        # get username and password from user input
        uid, pw = uid_entry.get(), pw_entry.get()
        # check if all fields are filled
        if not uid or not pw:
            messagebox.showerror("Error", "Please fill all fields.")
            return
        # call Library's login method to log in
        success, msg = lib.login(uid, pw)
        # if login sucessful, close the login window and open menu window
        if success:
            messagebox.showinfo("Success", msg)
            win.destroy()
            menu_window()
        else:
            messagebox.showerror("Error", msg)

    tk.Button(win, text="Login", command = do_login, width=15, height=2, font=("Arial", 20)).pack()

# allow user to search for books by title, author and ISBN
def search_book():
    # ask user for search keyword
    keyword = simpledialog.askstring("Search Book", "Enter title/author/ISBN: ")
    # call Library's search method
    if keyword:
        results = lib.search_book(keyword)
        # if no corresponding books found
        if not results:
            messagebox.showerror("Search Results", "No corresponding books found")
        # display search results
        else:
            display_text = "Search results:\n\n"
            for book in results:
                display_text = display_text + str(book) + "\n\n"
            messagebox.showinfo("Search Results", display_text)

# allow user to borrow a book by ISBN
def borrow_book():
    # get current user's username
    username = lib.current_user.get_username()
    # ask user for ISBN of the book to borrow
    ISBN = simpledialog.askstring("Borrow Book", "Enter ISBN of the book to borrow:")
    if not ISBN:
        return
    # call Library's borrow method and show result
    success, message = lib.borrow_book(username, ISBN)
    if success:
        messagebox.showinfo("Success", message)
    else:
        messagebox.showerror("Error", message)

# allow user to return a borrowed book
def return_book():
    # get current user's borrow records
    records = lib.current_user.get_borrow_records()
    if not records:
        messagebox.showinfo("Info", "You have no borrowed books.")
        return
    # list all borrowed books and ask user for book ID to return
    return_text = "Please input the Book ID you want to return:\n\n"
    for book_id in records:
        book = Book.get_book_by_id(book_id)
        return_text = return_text + str(book_id) + ". " + book.get_title() + "\n"
    book_id_str = simpledialog.askstring("Return Book", return_text)
    if not book_id_str:
        return
    # check if input ID is exists
    try:
        book_id = int(book_id_str)
        if book_id not in records:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Invalid Book ID.")
        return
    # call Library's return method and show result
    success, message = lib.return_book(lib.current_user.get_username(), book_id)
    if success:
        messagebox.showinfo("Success", message)
    else:
        messagebox.showerror("Error", message)

# display current user's borrow records
def view_borrow_records():
    # call Library's method to get current users' borrow records
    success, result = lib.view_borrow_records()
    if not success:
        messagebox.showerror("Error", result)
    else:
        # display result in messagebox
        if not result:
            messagebox.showinfo("Borrow Records", "No borrow records.")
        else:
            display_text = "Your borrowed books:\n\n"
            for line in result:
                display_text = display_text + line + "\n\n"
            messagebox.showinfo("Borrow Records", display_text)

# change other users' password(only for admin)
def change_password_admin():
    # ask for username who want to change the password
    target = simpledialog.askstring("Change Password", "Enter username to change password:")
    if not target:
        return

    if not User.exists(target):
        messagebox.showerror("Error", "Username not found.")
        return
    # ask for current password, for identify verification
    old_pw = simpledialog.askstring("Change Password", "Enter current password of that user:")
    if not old_pw:
        return
    # ask for new password
    new_pw = simpledialog.askstring("Change Password", "Enter new password:")
    if not new_pw:
        return
    # store the new password by calling Library's change password method
    success, message = lib.change_password(old_pw, new_pw, username=target)
    if success:
        messagebox.showinfo("Success", message)
    else:
        messagebox.showerror("Error", message)

# change other users' username(for admin)
def change_username_admin():
    # ask for username who want to change their username
    old_username = simpledialog.askstring("Change Username", "Enter current username:")
    if not old_username:
        return

    if not User.exists(old_username):
        messagebox.showerror("Error", "Username not found.")
        return
    # ask for new username
    new_username = simpledialog.askstring("Change Username", "Enter new username:")
    if not new_username:
        return
    # check if new username is already exist
    if User.exists(new_username):
        messagebox.showerror("Error", "New username is already taken.")
        return
    # when sucess, call  Library's change username method and show result
    success, message = lib.change_username(old_username, new_username)
    if success:
        messagebox.showinfo("Success", message)
    else:
        messagebox.showerror("Error", message)

# view any user's borrow records(for admin)
def view_any_records():
    # ask for username
    username = simpledialog.askstring("View Records", "Enter username to view borrow records:")
    if not username:
        return

    if not User.exists(username):
        messagebox.showerror("Error", "Username not found.")
        return
    # if success, call Library's method to get records and show result
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

# log out the current user and close menu window
def logout():
    # call Library's logout method
    success, msg = lib.logout()
    # if logout success, close menu window
    if success:
        messagebox.showinfo("Logout", msg)
        window = tk._default_root
        for widget in window.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()
    else:
        messagebox.showerror("Error", msg)

# allow user to change their own password
def change_own_pw():
    # ask for current password
    old_pw = simpledialog.askstring("Change Password", "Enter current password:")
    if not old_pw:
        messagebox.showerror("Error", "Please enter the current password.")
        return
    new_pw = simpledialog.askstring("Change Password", "Enter new password:")
    if not new_pw:
        messagebox.showerror("Error", "Please enter a new password.")
        return
    # if change success, call Librarys' change password method and show result
    success, message = lib.change_password(old_pw, new_pw)
    if success:
        messagebox.showinfo("Success", message)
    else:
        messagebox.showerror("Error", message)

# display the main menu after login successful
def menu_window():
    window = tk.Toplevel()
    window.geometry("600x600")
    window.title("Menu")
    # display welcome message
    tk.Label(window, text="Welcome " + lib.current_user.get_username(), width=25, height=2, font=("Arial", 20)).pack()
    # Normal User function buttons
    tk.Button(window, text="Search book", command = search_book, width = 20, height = 3, font=("Arial", 20)).pack()
    tk.Button(window, text="Borrow a book", command = borrow_book, width = 20, height = 3, font=("Arial", 20)).pack()
    tk.Button(window, text="Return book", command = return_book, width = 20, height = 3, font=("Arial", 20)).pack()
    tk.Button(window, text="Change password", command = change_own_pw, width = 20, height = 3, font=("Arial", 20)).pack()
    # check if the user has permissions, allow additional functions buttons for admin
    if lib.current_user.has_permission():
        tk.Button(window, text="Change another user's password", command = change_password_admin, width = 20, height = 3, font=("Arial", 20)).pack()
        tk.Button(window, text="View any user's borrow records", command = view_any_records, width = 20, height = 3, font=("Arial", 20)).pack()
    # logout button
    tk.Button(window, text = "Logout", command = logout, width = 20, height = 3, font=("Arial", 20)).pack()

if __name__ == "__main__":
    root = create_window()
    show_choice_frame(root)
    root.mainloop()
