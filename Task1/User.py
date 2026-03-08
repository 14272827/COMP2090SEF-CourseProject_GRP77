class User:
    users = {}
    def __init__(self, username="", password=""):
        self._username = username
        self._password = password
        self._books_records = []

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

    def set_username(self, username):
        self._username = username

    def set_password(self, password):
        self._password = password

    def register_user(self, username, pw, role="user"):
        if username in User.users:
            return False, "Username already exists, please try another one."
        else:
            User.users[username] = {
                "role": role,
                "password": pw,
                "books_data": []
            }
            self._username = username
            self._password = pw
            return True, "User created successfully."

    def change_password(self,pw, new_pw):
        if pw == self._password:
            self._password = new_pw
            User.users[self._username]["password"] = new_pw
            return True, "Password changed successfully."
        else:
            return False, "Incorrect password."

    def login(self, username, pw):
        if username in User.users and User.users[username]["password"] == pw:
            self.set_username(username)
            self.set_password(pw)
            self._books_records = User.users[username]["books_data"]
            return True, "Login successful."
        else:
            return False, "Incorrect username or password."

    def view_own_records(self):
        records = User.users[self._username]["books_data"]
        if not self._username:
            return False, "You have not logged in."
        if not records:
            return False, "You have no borrowed records."
        else:
            return True, records

    def logout(self):
        if self._username:
            self._username = ""
            self._password = ""
            return True, "Logout successful."

class Admin(User):
    def __init__(self,username,password):
        super().__init__(username,password)
