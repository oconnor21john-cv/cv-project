"""
BookList Module - manages the collection of books

This is basically a wrapper around a dictionary that stores Book objects.
Provides add, search, remove functionality.

Author: John
Software Development Module - Assignment 2
"""

from books import Books
from typing import Optional, List


class BookList:
    """
    Manages the library's book collection.
    
    Uses a dict with book_id as key for fast lookups.
    """
    
    def __init__(self):
        """Create empty book collection."""
        self._books = {}
    
    def add_book(self, book: Books) -> bool:
        """
        Add a book to the collection.
        Raises error if it's not a Books instance or ID already exists.
        """
        if not isinstance(book, Books):
            raise TypeError("Only Books instances can be added to the collection")
        
        book_id = book.get_book_id()
        if book_id in self._books:
            raise ValueError(f"A book with ID '{book_id}' already exists")
        
        self._books[book_id] = book
        return True
    
    def search_book(self, search_term: str, search_by: str = "title") -> List[Books]:
        """
        Search for books by title, author, publisher, or publication_date.
        Returns list of matching books (case-insensitive partial match).
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string")
        
        valid_fields = ['title', 'author', 'publisher', 'publication_date']
        search_by = search_by.lower()
        if search_by not in valid_fields:
            raise ValueError(f"Invalid search field. Use one of: {valid_fields}")
        
        search_term = search_term.lower().strip()
        results = []
        
        for book in self._books.values():
            # get the right attribute value
            if search_by == 'title':
                val = book.get_title().lower()
            elif search_by == 'author':
                val = book.get_author().lower()
            elif search_by == 'publisher':
                val = book.get_publisher().lower()
            else:  # publication_date
                val = book.get_publication_date().lower()
            
            if search_term in val:
                results.append(book)
        
        return results
    
    def remove_book(self, title: str) -> bool:
        """
        Remove a book by title.
        If multiple books have same title, warns and removes first match.
        """
        if not isinstance(title, str):
            raise TypeError("Title must be a string")
        if not title.strip():
            raise ValueError("Title cannot be empty")
        
        title_lower = title.lower().strip()
        
        # find matching books
        matches = []
        for book_id, book in self._books.items():
            if book.get_title().lower() == title_lower:
                matches.append((book_id, book))
        
        if not matches:
            raise ValueError(f"No book with title '{title}' found")
        
        if len(matches) > 1:
            print(f"Warning: Found {len(matches)} books with title '{title}':")
            for bid, b in matches:
                print(f"  - ID: {bid}, Author: {b.get_author()}")
            print("Removing first match...")
        
        # remove first match
        book_id_to_remove = matches[0][0]
        del self._books[book_id_to_remove]
        print(f"Book '{title}' (ID: {book_id_to_remove}) removed.")
        return True
    
    def get_total_books(self) -> int:
        """Return total number of books."""
        return len(self._books)
    
    def get_all_books(self) -> List[Books]:
        """Return list of all books."""
        return list(self._books.values())
    
    def get_book_by_id(self, book_id: str) -> Optional[Books]:
        """Get a book by its ID. Returns None if not found."""
        if not isinstance(book_id, str):
            raise TypeError("Book ID must be a string")
        return self._books.get(book_id, None)
    
    def display_all_books(self) -> None:
        """Print all books in a nice format."""
        if not self._books:
            print("No books in the collection.")
            return
        
        print(f"\n{'='*60}")
        print(f"LIBRARY BOOK COLLECTION - Total: {len(self._books)} books")
        print(f"{'='*60}")
        
        for i, book in enumerate(self._books.values(), 1):
            print(f"\n--- Book {i} ---")
            print(book)
        
        print(f"\n{'='*60}")
    
    def __str__(self) -> str:
        return f"BookList containing {len(self._books)} books"
    
    def __repr__(self) -> str:
        return f"BookList(books={list(self._books.keys())})"


# testing
if __name__ == "__main__":
    book_list = BookList()
    
    try:
        # add some books
        book1 = Books("Python Programming", "John Smith", 2023, "Tech Books Ltd", 5, "15-06-2023")
        book2 = Books("Data Science Fundamentals", "Jane Doe", 2022, "Academic Press", 3, "20-03-2022")
        book3 = Books("Machine Learning Basics", "John Smith", 2024, "Tech Books Ltd", 4, "10-01-2024")
        
        book_list.add_book(book1)
        book_list.add_book(book2)
        book_list.add_book(book3)
        
        book_list.display_all_books()
        
        # search test
        print("\nSearching for author 'John Smith':")
        for b in book_list.search_book("John Smith", "author"):
            print(f"  Found: {b.get_title()}")
        
        print(f"\nTotal: {book_list.get_total_books()}")
        
        # remove test
        print("\nRemoving 'Data Science Fundamentals'...")
        book_list.remove_book("Data Science Fundamentals")
        print(f"Total after removal: {book_list.get_total_books()}")
        
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
