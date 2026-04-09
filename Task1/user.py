#User.py
#This modules defines the User abstract parent class and it's child classes NormalUser and Admin
#It manages the user dictionary

#import the abc module for creating abstract class
from abc import ABC, abstractmethod

class User(ABC):
    #class attribute : user dictionary with username as key and user object as value
    users = {}
    
    #object attributes : each user's username, password and list of book id of books borrowed
    def __init__(self, username, pw):
        self._username = username
        self._password = pw
        self._borrow_records = [] #this stores the unique book id for all books borrowed by this user
    
    #Getters for encapsulation
    def get_username(self):
        return self._username
        
    def get_borrow_records(self):
        # list() returns a copy of the borrow records to prevent external modification since list is mutable
        return list(self._borrow_records)
    
    #classmethods for managing the user dictionary
    @classmethod
    def add_user(cls, username, user):
        cls.users[username] = user
    
    @classmethod
    def remove_user(cls, username):
        del cls.users[username]
    
    #classmethod to check if username exists in user dictionary
    @classmethod
    def exists(cls, username):
        return username in cls.users
    
    #classmethod for getting user object using username
    @classmethod
    def get_user(cls, username):
        return cls.users.get(username)
    
    #abstractmethods that child classes must have
    @abstractmethod
    def get_role(self):
        #return the role in string "Normal User" or "Admin"
        pass
    
    @abstractmethod
    def has_permission(self):
        #return True if the user is Admin, False if not
        pass
    
    #check if password is correct (called in library for login and change_password)
    def check_password(self, pw):
        return self._password == pw
    
    #change password
    def change_password(self, new_pw):
        self._password = new_pw
    
    #change username
    def change_username(self, new_username):
        User.remove_user(self.get_username()) #calls the classmethod to remove user from user dictionary
        self._username = new_username
        User.add_user(new_username,  self) #calls the classmethod to add user to user dictionary
    
    #add borrowed book's book id to user's _borrow_records
    def add_borrow_record(self, book_id):
        self._borrow_records.append(book_id)
    
    #remove book id in user's _borrow_records after return_book in library
    def remove_borrow_record(self, book_id):
        self._borrow_records = [b_id for b_id in self._borrow_records if b_id != book_id]

#child classes
class NormalUser(User):
    def get_role(self):
        return "Normal User"
    
    def has_permission(self):
        #return False since NormalUsers do not have admin permission 
        return False
    
class Admin(User):
    def get_role(self):
        return "Admin"
    
    def has_permission(self):
        #return True, admin has permission
        return True
        
