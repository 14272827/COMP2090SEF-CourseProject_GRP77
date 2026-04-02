class Book:
    book_catalog = []
    current_id = 1
    
    def __init__(self,title, author, ISBN):
        self._title = title
        self._author = author
        self._ISBN = ISBN
        self._available = True
        self._borrowed_by = None
        self._due_date = None
        self._id = Book.current_id
        Book.add_to_catalog(self)
        Book.update_current_id()
        
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
        
    def borrow_book(self, username, due_date):
        self._available = False
        self._borrowed_by = username
        self._due_date = due_date
        
    def return_book(self):
        self._available = True
        self._borrowed_by = None
        self._due_date = None
    
    @classmethod
    def add_to_catalog(cls, book):
        cls.book_catalog.append(book)
    
    @classmethod
    def update_current_id(cls):
        cls.current_id += 1
        
    @classmethod
    def get_available_by_ISBN(cls, ISBN):
        for b in cls.book_catalog:
            if b.get_ISBN() == ISBN and b.is_available():
                return b
        return None
    
    @classmethod
    def get_book_by_id(cls, book_id):
        for b in cls.book_catalog:
            if b.get_id() == book_id:
                return b
        return None
    
    
    @classmethod
    def search_book(cls, keyword):
        if not keyword:
            return []
        
        keyword = keyword.strip().lower()
        return [
            b for b in cls.book_catalog 
        if keyword in b.get_title().lower() 
        or keyword in b.get_author().lower() 
        or keyword in b.get_ISBN()
        ]
        
    def __str__(self):
        if self.is_available():
            status = "Available"
        else:
            status = "Borrowed"
            
        return ("[ID: " + str(self.get_id()) + "] " + self.get_title() + " by " + self.get_author()
        + " ISBN: " + self.get_ISBN() + " Status: " + status)
        
        
        
        
        
        
        
        
        
        
        
  