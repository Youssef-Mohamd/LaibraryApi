from fastapi import FastAPI # type: ignore
from pydantic import BaseModel , Field # type: ignore
from datetime import datetime
from typing import List
# Create FastAPI instance
server=FastAPI()

# url=> http://localhost:8000

# standerd response model
class StandardResponse(BaseModel):
    success: bool
    message: str
    data: dict = {}  # Default empty dictionary

# function to create standard response
def create_response(success: bool, message: str, data: dict = {}) :
     return StandardResponse(success=success, message=message, data=data)


# Book model
class Book(BaseModel):
        id: int
        title: str
        author:str
        available_copies: int

class BorrowRequest(BaseModel):
    book_id: int
    user_id: str

# Borrow Record model
class BorrowRecord(BaseModel):
    book_id: int
    user_id: str
    book_title: str
    borrow_date: datetime = Field(default_factory=datetime.now)

# Sample Data - List of Book objects
books_db = [
    Book(id=1, title="Clean Code", author="Robert C. Martin", available_copies=4),
    Book(id=2, title="The Pragmatic Programmer", author="Andrew Hunt", available_copies=2),
    Book(id=3, title="Design Patterns", author="Erich Gamma", available_copies=3)
]

# List to store borrowed books
borrowed_books = []

 ################### GET Request ########################
@server.get("/")
def health():
    return {"health" :"ok" ,"status": "success"}

# Get all books
@server.get("/books")
def getAllBooks():
     return create_response(True, "Books retrieved successfully", {"books": books_db})

# Get book by ID
@server.get("/books/{book_id}")
def getBookById(book_id):
     for book in books_db:
          if book.id == int(book_id):
               return create_response(True, "Book retrieved successfully", {"book": book})
     return create_response(False, "Book not found")


      ##################### Post Requests #########################

# Add a new book
@server.post("/books", response_model=StandardResponse)
def addBook(book: Book):
     for b in books_db:
          if b.id == book.id:
                return create_response(False, "Book with this ID already exists")
          
     books_db.append(book)
     return create_response(True, "Book added successfully", {"book": book})

     
      ################### Update Requests ########################
#update book by ID => Path parameter

@server.put("/books/{book_id}")
def updateBook(book_id: int, updated_book:Book):
     for index, book in enumerate(books_db): # Iterate with index
            if book.id == book_id: # Check if current book has the same ID
             updated_book.id = book_id
             books_db[book_id] = updated_book
            return create_response(True, "Book updated successfully", {"book": updated_book})
     return create_response(False, "Book not found")

    ################### Delete Requests ########################
    # Delete book by ID
@server.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books_db): # Iterate with index
       if book.id == book_id:  # Check if current book has the same ID
        deleted_book = books_db.pop(book_id) # Remove book from list using its index
        return create_response(True, "Book deleted", {"book": deleted_book})
    return create_response(False, "Book not found")

    ################### Borrow Requests ########################
@server.post("/borrow")
def borrowBook(request: BorrowRequest):
     
     for book in books_db:
          if book.id == request.book_id:   #find book
               if book.available_copies <= 0:    # Check if book is available
                    return create_response(False, "No copies available")
               
               book.available_copies -= 1        # Reduce available copies
                   
               borrow_record = BorrowRecord(         #create record => help in return process
                book_id=request.book_id,
                user_id=request.user_id,
                book_title=book.title
            )
               borrowed_books.append(borrow_record)
               return create_response( True,
                    f"Book '{book.title}' borrowed successfully",
                    {"available_copies": book.available_copies}
               )
     return create_response(False, "Book not found")

   ######################## Return Requests ########################
   
@server.post("/return")
def returnBook(request: BorrowRequest):
     for i, record in enumerate(borrowed_books): # Iterate with index 
          if record.book_id == request.book_id and record.user_id == request.user_id:
               for book in books_db:
                    if book.id == request.book_id:
                         book.available_copies += 1    # Increase available copies
                         returned_record = borrowed_books.pop(i)  # Remove borrow record
                         return create_response(
                              True,
                              f"Book '{book.title}' returned successfully",
                              {"available_copies": book.available_copies}
                         )
     return create_response(False, "Borrow record not found")
