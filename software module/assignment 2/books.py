"""
Books Module for the Library System


Software Development Module - Assignment 2
"""

import random
import string
from datetime import datetime


class Books:
    """
    Represents a single book in the library.
    
    Each book has a unique ID (randomly generated), plus all the usual
    info like title, author, publication year, etc. We also track how
    many copies we have and how many are currently available.
    """
    
    def __init__(self, title: str, author: str, year: int, publisher: str,
                 num_copies: int, publication_date: str):
        """
        Create a new book with the given details.
        
        The book_id is auto-generated so you don't need to pass it in.
        All the other fields get validated to make sure they're sensible.
        """
        # generate unique ID first
        self._book_id = self._generate_book_id()
        
        # use setters for validation
        self.set_title(title)
        self.set_author(author)
        self.set_year(year)
        self.set_publisher(publisher)
        self.set_num_copies(num_copies)
        
        # when first added, all copies are available
        self._available_copies = self._num_copies
        
        self.set_publication_date(publication_date)
    
    def _generate_book_id(self) -> str:
        """Generate a random ID like 'BK-A1B2C3D4'"""
        chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return f"BK-{chars}"
    
    # --- Setters ---
    
    def set_title(self, title: str) -> None:
        """Set book title. Can't be empty."""
        if not isinstance(title, str):
            raise TypeError("Title must be a string")
        if not title.strip():
            raise ValueError("Title cannot be empty")
        self._title = title.strip()
    
    def set_author(self, author: str) -> None:
        """Set author name. Can't be empty."""
        if not isinstance(author, str):
            raise TypeError("Author must be a string")
        if not author.strip():
            raise ValueError("Author cannot be empty")
        self._author = author.strip()
    
    def set_year(self, year: int) -> None:
        """Set publication year. Must be between 1000 and current year."""
        if not isinstance(year, int):
            raise TypeError("Year must be an integer")
        current_year = datetime.now().year
        if year < 1000 or year > current_year:
            raise ValueError(f"Year must be between 1000 and {current_year}")
        self._year = year
    
    def set_publisher(self, publisher: str) -> None:
        """Set publisher name."""
        if not isinstance(publisher, str):
            raise TypeError("Publisher must be a string")
        if not publisher.strip():
            raise ValueError("Publisher cannot be empty")
        self._publisher = publisher.strip()
    
    def set_num_copies(self, num_copies: int) -> None:
        """Set total number of copies. Can't be negative."""
        if not isinstance(num_copies, int):
            raise TypeError("Number of copies must be an integer")
        if num_copies < 0:
            raise ValueError("Number of copies cannot be negative")
        self._num_copies = num_copies
    
    def set_available_copies(self, available_copies: int) -> None:
        """Set available copies. Can't exceed total or be negative."""
        if not isinstance(available_copies, int):
            raise TypeError("Available copies must be an integer")
        if available_copies < 0:
            raise ValueError("Available copies cannot be negative")
        if available_copies > self._num_copies:
            raise ValueError("Available copies cannot exceed total copies")
        self._available_copies = available_copies
    
    def set_publication_date(self, publication_date: str) -> None:
        """Set publication date in DD-MM-YYYY format."""
        if not isinstance(publication_date, str):
            raise TypeError("Publication date must be a string")
        # try parsing to validate format
        try:
            datetime.strptime(publication_date, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Publication date must be in DD-MM-YYYY format")
        self._publication_date = publication_date
    
    # --- Getters ---
    
    def get_book_id(self) -> str:
        return self._book_id
    
    def get_title(self) -> str:
        return self._title
    
    def get_author(self) -> str:
        return self._author
    
    def get_year(self) -> int:
        return self._year
    
    def get_publisher(self) -> str:
        return self._publisher
    
    def get_num_copies(self) -> int:
        return self._num_copies
    
    def get_available_copies(self) -> int:
        return self._available_copies
    
    def get_publication_date(self) -> str:
        return self._publication_date
    
    # --- Other methods ---
    
    def __str__(self) -> str:
        return (f"Book ID: {self._book_id}\n"
                f"Title: {self._title}\n"
                f"Author: {self._author}\n"
                f"Year: {self._year}\n"
                f"Publisher: {self._publisher}\n"
                f"Total Copies: {self._num_copies}\n"
                f"Available Copies: {self._available_copies}\n"
                f"Publication Date: {self._publication_date}")
    
    def __repr__(self) -> str:
        return f"Books(id='{self._book_id}', title='{self._title}', author='{self._author}', year={self._year})"


# quick test
if __name__ == "__main__":
    try:
        book = Books(
            title="Python Programming",
            author="John Smith",
            year=2023,
            publisher="Tech Books Ltd",
            num_copies=5,
            publication_date="15-06-2023"
        )
        print("Book created!")
        print(book)
        print()
        print(f"ID: {book.get_book_id()}")
        print(f"Available: {book.get_available_copies()}")
        
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
