from abc import ABC, abstractmethod

class User(ABC):
    users = {}
    
    def __init__(self, username, pw):
        self._username = username
        self._password = pw
        self._borrow_records = []
    
    def get_username(self):
        return self._username
        
    def get_borrow_records(self):
        return list(self._borrow_records)
        
    @classmethod
    def add_user(cls, username, user):
        cls.users[username] = user
    
    @classmethod
    def remove_user(cls, username):
        del cls.users[username]
        
    @classmethod
    def exists(cls, username):
        return username in cls.users
        
    @classmethod
    def get_user(cls, username):
        return cls.users.get(username)
    
    @abstractmethod
    def get_role(self):
        pass
    
    @abstractmethod
    def has_permission(self):
        pass
    
    def check_password(self, pw):
        return self._password == pw

    def change_password(self, new_pw):
        self._password = new_pw
    
    def change_username(self, new_username):
        User.remove_user(self.get_username())
        self._username = new_username
        User.add_user(new_username,  self)
        
    def add_borrow_record(self, book_id):
        self._borrow_records.append(book_id)
        
    def remove_borrow_record(self, book_id):
        self._borrow_records = [b_id for b_id in self._borrow_records if b_id != book_id]
    
class NormalUser(User):
    def get_role(self):
        return "Normal User"
    
    def has_permission(self):
        return False
    
class Admin(User):
    def get_role(self):
        return "Admin"
    
    def has_permission(self):
        return True
    
    
    
    
    
    
    
    
    
    
    
        
