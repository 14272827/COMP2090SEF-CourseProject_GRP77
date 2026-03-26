import tkinter as tk
from tkinter import messagebox
from User import NormalUser, Admin

class LoginGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Library Management System")
        self.window.geometry("400x300")
        self.font = ("Times New Roman", 15)
        self.title_font = ("Times New Roman", 20, "bold")
        self.create_users()
        self.setup()

    # testing acc(admin)
    def create_users(self):
        admin = Admin()
        admin.register_user("admin123", "654321", "admin")

    def setup(self):
        title = tk.Label(self.window, text="Library System", font=self.title_font)
        title.pack(pady=10)

        tk.Label(self.window, text="Username:", font=self.font).pack()
        self.username_entry = tk.Entry(self.window, font=self.font)
        self.username_entry.pack()

        tk.Label(self.window, text="Password:", font=self.font).pack()
        self.password_entry = tk.Entry(self.window, font=self.font)
        self.password_entry.pack()

        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Login", command=self.login, font=self.font).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Register", command=self.show_register, font=self.font).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Exit", command=self.window.quit, font=self.font).pack(side=tk.LEFT, padx=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Warning", "Please input both username and password")
            return

        user = NormalUser()
        success, message = user.login(username, password)

        if success:
            messagebox.showinfo("Success", "Welcome" + username)
            self.window.destroy()
        else:
            messagebox.showerror("Error", message)
            self.password_entry.delete(0, tk.END)

    def show_register(self):
        reg_window = tk.Toplevel(self.window)
        reg_window.title("Register")
        reg_window.geometry("400x300")

        tk.Label(reg_window, text="Register (For Normal User)", font=self.title_font).pack(pady=10)

        tk.Label(reg_window, text="Username:", font=self.font).pack()
        reg_username = tk.Entry(reg_window, font=self.font)
        reg_username.pack()

        tk.Label(reg_window, text="Password:", font=self.font).pack()
        reg_password = tk.Entry(reg_window, font=self.font)
        reg_password.pack()

        def register():
            username = reg_username.get()
            password = reg_password.get()

            if not username or not password:
                messagebox.showwarning("Warning", "Please input both username or password")
                return

            user = NormalUser()
            success, message = user.register_user(username, password, "user")

            if success:
                messagebox.showinfo("Success", message)
                reg_window.destroy()
            else:
                messagebox.showerror("Error", message)

        tk.Button(reg_window, text="Register", command=register, font=self.font).pack(pady=10)

    def run(self):
        self.window.mainloop()

app = LoginGUI()
app.run()
