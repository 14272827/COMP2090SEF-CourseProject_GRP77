#book.py
#This module define the Book class and manages the book catalog
#Each book object is a unique physical copy

class Book:
    #class attribute : list of all the books
    book_catalog = []
    #class attribute : the current book id for a new book (auto-increment)
    current_id = 1

    #object attributes : each book's own title, author , ISBN, availability, borrow status, due date and unique id
    def __init__(self,title, author, ISBN):
        self._title = title
        self._author = author
        self._ISBN = ISBN
        self._available = True #True = not borrowed , False = borrowed
        self._borrowed_by = None #if borrowed, stores username of the user that borrowed the book
        self._due_date = None #due date if the book is borrowed, date object
        self._id = Book.current_id
        Book.add_to_catalog(self) #call the classmethod to add this book to the catalog
        Book.update_current_id()  #call the classmethod for id increment
    
    #Getters for encapsulation
    def get_title(self):
        return self._title
        
    def get_author(self):
        return self._author
        
    def get_ISBN(self):
        return self._ISBN
        
    def is_available(self):
        return self._available
    
    def get_borrowed_by(self):
        return self._borrowed_by
    
    def get_due_date(self):
        return self._due_date
        
    def get_id(self):
        return self._id
        
    #borrow/return methods called in library
    def borrow_book(self, username, due_date):
        self._available = False
        self._borrowed_by = username
        self._due_date = due_date
        
    def return_book(self):
        self._available = True
        self._borrowed_by = None
        self._due_date = None
    
    #classmethod for appending the book object to the catalog
    @classmethod
    def add_to_catalog(cls, book):
        cls.book_catalog.append(book)
    
    #classmethod for id increment
    @classmethod
    def update_current_id(cls):
        cls.current_id += 1
    
    #classmethod to get available book by ISBN(for borrow_book in library)
    @classmethod
    def get_available_by_ISBN(cls, ISBN):
        #return the first book available with matching ISBN, if not return None
        for b in cls.book_catalog:
            if b.get_ISBN() == ISBN and b.is_available():
                return b
        return None
    
    #classmethod to get book object by id
    @classmethod
    #return the book object with matching id, if not return None
    def get_book_by_id(cls, book_id):
        for b in cls.book_catalog:
            if b.get_id() == book_id:
                return b
        return None
    
    #classmethod for searching book in the catalog(called in library)
    @classmethod
    def search_book(cls, keyword):
        #search book with keyword in title, author, ISBN, case-insensitive(used .lower())
        #return a list of matching books, if not an empty list
        
        if not keyword:
            return []
        
        keyword = keyword.strip().lower()
        return [
            b for b in cls.book_catalog 
        if keyword in b.get_title().lower() 
        or keyword in b.get_author().lower() 
        or keyword in b.get_ISBN()
        ]
    
    #magicmethod for printing out book objects that shows the details
    def __str__(self):
        if self.is_available():
            status = "Available"
        else:
            status = "Borrowed"
            
        return ("[ID: " + str(self.get_id()) + "] " + self.get_title() + " by " + self.get_author()
        + " ISBN: " + self.get_ISBN() + " Status: " + status)
