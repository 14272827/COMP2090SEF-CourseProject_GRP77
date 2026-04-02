from datetime import date, timedelta
from user import User, NormalUser, Admin
from book import Book

class Library():
    admin_code = "COMP2090SEF"
    loan_period = 14
    overdue_fine = 1.5
    max_fine = 130
    
    def __init__(self):
        self.current_user = None
    
    @staticmethod
    def check_ISBN(ISBN):
        ISBN = ISBN.replace("-", "")
        return ISBN.isdigit() and len(ISBN) in [10, 13]
    
    def register_user(self, username, pw, role = "user", code = None):
        if User.exists(username):
            return False, "Username already exists. Please try another one."
        
        if role.lower() == "admin":
            if code != self.admin_code:
                return False, "Incorrect Admin code."
                
            user = Admin(username, pw)
            
        else:
            user = NormalUser(username, pw)
        
        User.add_user(username, user)
        return True, user.get_role() + " account registered successfully."
        
    def login(self,username, pw):
        user = User.get_user(username)
        if user and user.check_password(pw):
            self.current_user = user
            return True, "Logged in as " + username
        else:
            return False, "Incorrect username or password."
    
    def logout(self):
        if not self.current_user:
            return False, "No User is logged in."
            
        self.current_user = None
        return True, "Logout successful."
    
    def change_username(self, old_username, new_username):
        if not self.current_user or not self.current_user.has_permission():
            return False, "You do not have permission to change username."
            
        if not User.exists(old_username):
            return False, "Username not found."
        
        if User.exists(new_username):
            return False, "New username is already taken."
        
        user =  User.get_user(old_username)
        user.change_username(new_username)
        
        return True, "Username changed successfully."
        
    def change_password(self, pw, new_pw, username=None):
        if not self.current_user:
            return False, "You must be logged in first to change password."
            
        if username is None:
            username = self.current_user.get_username()
        
        if not self.current_user.has_permission() and username != self.current_user.get_username():
            return False, "You are only allowed to change your own password."
            
        user = User.get_user(username)
        if not user:
            return False, "Username not found."
        
        if user.check_password(pw):
            user.change_password(new_pw)
            return True, "Password has been changed successfully."
        else:
            return False, "Incorrect password."
     
    def search_book(self, keyword):
        return Book.search_book(keyword)
        
    def borrow_book(self, username, ISBN):
        if not User.exists(username):
            return False, "Username not found."
        
        if not self.check_ISBN(ISBN):
            return False, "Invalid ISBN."
            
        book = Book.get_available_by_ISBN(ISBN)
        if not book:
            return False, "No available copies of this book."
        
        due_date = date.today() + timedelta(days = self.loan_period)
        
        user = User.get_user(username)
        user.add_borrow_record(book.get_id())

        book.borrow_book(username, due_date)

        
        return True, ("Book borrowed successfully. Title: " + book.get_title() +
        " Due date: " + due_date.strftime("%Y-%m-%d"))

    def return_book(self, username, book_id):
        if not User.exists(username):
            return False, "Username not found."
            
        book = Book.get_book_by_id(book_id)
        if not book or username != book.get_borrowed_by():
            return False, "You have not borrowed this book."
            
        fine = 0
        due_date = book.get_due_date()
        now_date = date.today()
        
        if now_date > due_date:
            overdue_days = (now_date - due_date).days
            fine = overdue_days * self.overdue_fine
            fine = round(fine, 1)
            if fine > self.max_fine:
                fine = self.max_fine
        
        book.return_book()
        
        user = User.get_user(username)
        user.remove_borrow_record(book_id)
        
        return True, "Book returned successfully. Title: " + book.get_title() + " Fine: HK$" + str(fine)
    
    def view_borrow_records(self, username = None):
        if not self.current_user:
            return False, "You must log in first"
            
        if not username:
            user = self.current_user
        else:
            user = User.get_user(username)
        
        if not user:
            return False, "User not found"
        
        if user !=  self.current_user and not self.current_user.has_permission():
            return False, "You can only view your own records"
            
        records = user.get_borrow_records()
        if not records:
            return False, "No borrow records."
        
        result = []
        for b_id in records:
            b = Book.get_book_by_id(b_id)
            result.append("[ID: " + str(b.get_id()) + "] " + b.get_title() + " by " + b.get_author()
        + " ISBN: " + b.get_ISBN() + " Due_date: " + b.get_due_date().strftime("%Y-%m-%d"))
        
        return True, result
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

 