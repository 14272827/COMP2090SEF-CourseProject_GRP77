#library.py
#This module defines the Library class which is the core system

#import date object, timedelta from datetime module for due date(fine calculation)
from datetime import date, timedelta
#import user
from user import User, NormalUser, Admin
#import book
from book import Book

class Library():
    #class variables : store variables for configuration
    admin_code = "COMP2090SEF" #code needed to register admin account
    loan_period = 14 #days a book can be borrowed (from Hong Kong Public Libraries)
    overdue_fine = 1.5 #HK$ per day overdue (from Hong Kong Public Libraries)
    max_fine = 130 #maximum fine per book (from Hong Kong Public Libraries)
    
    def __init__(self):
        self.current_user = None #current logged in user, None if not logged in
    
    #staticmethod for checking ISBN, after stripping hyphens, ISBN should be digits with length 10 or 13
    @staticmethod
    def check_ISBN(ISBN):
        ISBN = ISBN.replace("-", "")
        return ISBN.isdigit() and len(ISBN) in [10, 13]
    
    #registration
    def register_user(self, username, pw, role = "user", code = None):
        #check if username already exists
        if User.exists(username):
            return False, "Username already exists. Please try another one."
        
        #check admin code if registering an admin account
        if role.lower() == "admin":
            if code != self.admin_code:
                return False, "Incorrect Admin code."
            
            #create user objects
            user = Admin(username, pw)
            
        else:
            user = NormalUser(username, pw)
        
        #call the User classmethod to add user to user dictionary
        User.add_user(username, user)
        return True, user.get_role() + " account registered successfully."
    
    #login
    def login(self,username, pw):
        #get user object and check if it exists and it's password
        user = User.get_user(username)
        if user and user.check_password(pw):
            self.current_user = user
            return True, "Logged in as " + username
        else:
            return False, "Incorrect username or password."
    
    #logout
    def logout(self):
        #logout if logged in
        if not self.current_user:
            return False, "No User is logged in."
            
        self.current_user = None
        return True, "Logout successful."
    
    #change username
    def change_username(self, old_username, new_username):
        #needs to be logged in and admin to change username
        if not self.current_user or not self.current_user.has_permission():
            return False, "You do not have permission to change username."
        
        #check if old username exists
        if not User.exists(old_username):
            return False, "Username not found."
        
        #check if new username exists
        if User.exists(new_username):
            return False, "New username is already taken."
        
        user =  User.get_user(old_username) #get user object with old username
        user.change_username(new_username) #call  User method to change old username to new
        
        return True, "Username changed successfully."
    
    #change password
    def change_password(self, pw, new_pw, username=None):
        #check if logged in
        if not self.current_user:
            return False, "You must be logged in first to change password."
            
        #if not specified username, default to current user
        if username is None:
            username = self.current_user.get_username()
            
        #admin needed to change other's password
        if not self.current_user.has_permission() and username != self.current_user.get_username():
            return False, "You are only allowed to change your own password."
        
        #get the user object
        user = User.get_user(username)
        #check if user exists
        if not user:
            return False, "Username not found."
            
        #check if correct password or not
        if user.check_password(pw):
            user.change_password(new_pw) #calls the User method to change password
            return True, "Password has been changed successfully."
        else:
            return False, "Incorrect password."
     
    #search book using keyword
    def search_book(self, keyword):
        return Book.search_book(keyword) #calls the Book classmethod to search book with given keyword
    
    #borrow book 
    def borrow_book(self, username, ISBN):
        #check if username exists in user dictionary
        if not User.exists(username):
            return False, "Username not found."
        
        #check if given ISBN is valid
        if not self.check_ISBN(ISBN):
            return False, "Invalid ISBN."
        
        #call Book classmethod to get first available book with matching ISBN
        book = Book.get_available_by_ISBN(ISBN)
        #check if there are available book
        if not book:
            return False, "No available copies of this book."
        
        #calculate due date, today + loan_period
        due_date = date.today() + timedelta(days = self.loan_period)
        
        user = User.get_user(username) #get user object
        user.add_borrow_record(book.get_id()) #call User method to add book id to borrow_record

        book.borrow_book(username, due_date) #call Book method to add borrower's username and due date

        
        return True, ("Book borrowed successfully. Title: " + book.get_title() +
        " Due date: " + due_date.strftime("%Y-%m-%d"))
        
    #return book
    def return_book(self, username, book_id):
        #check if username exists in user dictionary
        if not User.exists(username):
            return False, "Username not found."
        
        #get book object by book id
        book = Book.get_book_by_id(book_id)
        #check if book exists and if borrowe record matches
        if not book or username != book.get_borrowed_by():
            return False, "You have not borrowed this book."
        
        #calculate fine
        fine = 0
        due_date = book.get_due_date() #get due date
        now_date = date.today() #create date object with date today 
        
        #check if today > due date
        if now_date > due_date:
            overdue_days = (now_date - due_date).days #today - due date to get days overdue
            fine = overdue_days * self.overdue_fine #days overdue * overdue fine = fine
            fine = round(fine, 1) #round to 1 decimal to avoid weird presentation
            #check if fine > maximum fine
            if fine > self.max_fine:
                fine = self.max_fine
        
        book.return_book() #call Book method to return book
        
        user = User.get_user(username) #get user object
        user.remove_borrow_record(book_id) #remove book id from user's borrow record
        
        return True, "Book returned successfully. Title: " + book.get_title() + " Fine: HK$" + str(fine)
    
    #view own or others borrow records
    def view_borrow_records(self, username = None):
        #check if logged in
        if not self.current_user:
            return False, "You must log in first"
        
        #if no specified username, default to current user
        if not username:
            user = self.current_user
        else:
            user = User.get_user(username)
        
        #check if user exists
        if not user:
            return False, "User not found"
        
        #admin needed to view other's records
        if user !=  self.current_user and not self.current_user.has_permission():
            return False, "You can only view your own records"
            
        records = user.get_borrow_records() #get borrow records
        if not records:
            return False, "No borrow records."
        
        #store each borrow records' detail in result 
        result = []
        for b_id in records:
            b = Book.get_book_by_id(b_id) #get book object by book id
            result.append("[ID: " + str(b.get_id()) + "] " + b.get_title() + " by " + b.get_author()
        + " ISBN: " + b.get_ISBN() + " Due_date: " + b.get_due_date().strftime("%Y-%m-%d"))
        
        return True, result #print out results in a list
