"""
Loans Module

Tracks which users have borrowed which books, calculates due dates,
and can report on overdue items.

Software Development Module - Assignment 2
"""

from datetime import datetime, timedelta
from typing import Dict, List
from books import Books
from users import Users
from booklist import BookList
from userlist import UserList


class Loans:
    """
    Manages book loans.
    
    Stores loans as dict with (username, book_id) tuple as key.
    Needs references to BookList and UserList to validate operations.
    """
    
    def __init__(self, book_list: BookList, user_list: UserList, loan_period_days: int = 14):
        """
        Set up the loans system.
        
        Args:
            book_list: the library's book collection
            user_list: the library's user collection  
            loan_period_days: how long users can borrow for (default 14 days)
        """
        if not isinstance(book_list, BookList):
            raise TypeError("book_list must be a BookList instance")
        if not isinstance(user_list, UserList):
            raise TypeError("user_list must be a UserList instance")
        if not isinstance(loan_period_days, int) or loan_period_days <= 0:
            raise ValueError("Loan period must be a positive integer")
        
        self._loans = {}  # key: (username, book_id), value: loan info dict
        self._book_list = book_list
        self._user_list = user_list
        self._loan_period_days = loan_period_days
    
    def borrow_book(self, username: str, book_id: str) -> bool:
        """
        Borrow a book for a user.
        
        Checks user exists, book exists, copies available, and user
        doesn't already have this book. Then creates the loan record
        and decrements available copies.
        """
        if not isinstance(username, str):
            raise TypeError("Username must be a string")
        if not isinstance(book_id, str):
            raise TypeError("Book ID must be a string")
        
        username = username.strip()
        book_id = book_id.strip()
        
        # check user exists
        user = self._user_list.get_user_by_username(username)
        if user is None:
            raise ValueError(f"User '{username}' does not exist")
        
        # check book exists
        book = self._book_list.get_book_by_id(book_id)
        if book is None:
            raise ValueError(f"Book with ID '{book_id}' does not exist")
        
        # check not already borrowed by this user
        loan_key = (username, book_id)
        if loan_key in self._loans:
            raise ValueError(f"User '{username}' already has this book")
        
        # check availability
        available = book.get_available_copies()
        if available <= 0:
            raise ValueError(f"No copies of '{book.get_title()}' available")
        
        # create loan record
        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=self._loan_period_days)
        
        self._loans[loan_key] = {
            'borrow_date': borrow_date,
            'due_date': due_date,
            'book_title': book.get_title(),
            'user_firstname': user.get_firstname()
        }
        
        # update book availability
        book.set_available_copies(available - 1)
        
        print(f"SUCCESS: '{book.get_title()}' borrowed by {user.get_full_name()}")
        print(f"Due date: {due_date.strftime('%d-%m-%Y')}")
        return True
    
    def return_book(self, username: str, book_id: str) -> bool:
        """
        Return a borrowed book.
        
        Removes loan record and increments available copies.
        Warns if the book was overdue.
        """
        if not isinstance(username, str):
            raise TypeError("Username must be a string")
        if not isinstance(book_id, str):
            raise TypeError("Book ID must be a string")
        
        username = username.strip()
        book_id = book_id.strip()
        
        loan_key = (username, book_id)
        if loan_key not in self._loans:
            raise ValueError(f"No loan found for user '{username}' and book '{book_id}'")
        
        # get book to update copies
        book = self._book_list.get_book_by_id(book_id)
        if book:
            book.set_available_copies(book.get_available_copies() + 1)
        else:
            print(f"Warning: Book '{book_id}' no longer in system")
        
        loan_info = self._loans[loan_key]
        book_title = loan_info['book_title']
        
        # check if overdue
        if datetime.now() > loan_info['due_date']:
            days_late = (datetime.now() - loan_info['due_date']).days
            print(f"NOTE: This book was {days_late} day(s) overdue!")
        
        del self._loans[loan_key]
        print(f"SUCCESS: '{book_title}' returned by '{username}'")
        return True
    
    def count_user_loans(self, username: str) -> int:
        """Count how many books a user currently has borrowed."""
        if not isinstance(username, str):
            raise TypeError("Username must be a string")
        username = username.strip()
        return sum(1 for (u, _) in self._loans.keys() if u == username)
    
    def get_user_loans(self, username: str) -> List[Dict]:
        """Get list of all books currently borrowed by a user."""
        if not isinstance(username, str):
            raise TypeError("Username must be a string")
        
        username = username.strip()
        result = []
        
        for (u, book_id), info in self._loans.items():
            if u == username:
                result.append({
                    'book_id': book_id,
                    'book_title': info['book_title'],
                    'borrow_date': info['borrow_date'],
                    'due_date': info['due_date'],
                    'is_overdue': datetime.now() > info['due_date']
                })
        
        return result
    
    def get_overdue_books(self) -> List[Dict]:
        """Get all overdue loans with user info."""
        overdue = []
        now = datetime.now()
        
        for (username, book_id), info in self._loans.items():
            if now > info['due_date']:
                days_overdue = (now - info['due_date']).days
                
                # get user firstname
                user = self._user_list.get_user_by_username(username)
                firstname = user.get_firstname() if user else info.get('user_firstname', 'Unknown')
                
                overdue.append({
                    'book_id': book_id,
                    'book_title': info['book_title'],
                    'username': username,
                    'user_firstname': firstname,
                    'borrow_date': info['borrow_date'],
                    'due_date': info['due_date'],
                    'days_overdue': days_overdue
                })
        
        return overdue
    
    def print_overdue_books(self) -> None:
        """
        Print report of overdue books.
        
        Shows book title, username and first name (retrieved via the
        User class methods as per assignment requirements).
        """
        overdue = self.get_overdue_books()
        
        if not overdue:
            print("\n*** No overdue books at this time ***")
            return
        
        print(f"\n{'='*70}")
        print(f"OVERDUE BOOKS REPORT - Total: {len(overdue)} overdue items")
        print(f"{'='*70}")
        print(f"{'Book Title':<30} {'Username':<15} {'First Name':<15} {'Days Overdue':<10}")
        print(f"{'-'*70}")
        
        for item in overdue:
            print(f"{item['book_title']:<30} {item['username']:<15} "
                  f"{item['user_firstname']:<15} {item['days_overdue']:<10}")
        
        print(f"{'='*70}")
    
    def get_total_active_loans(self) -> int:
        """Return total number of active loans."""
        return len(self._loans)
    
    def display_all_loans(self) -> None:
        """Print all active loans."""
        if not self._loans:
            print("\n*** No active loans ***")
            return
        
        print(f"\n{'='*80}")
        print(f"ACTIVE LOANS - Total: {len(self._loans)}")
        print(f"{'='*80}")
        print(f"{'Username':<15} {'Book Title':<30} {'Borrow Date':<12} {'Due Date':<12} {'Status':<10}")
        print(f"{'-'*80}")
        
        now = datetime.now()
        for (username, _), info in self._loans.items():
            borrow = info['borrow_date'].strftime('%d-%m-%Y')
            due = info['due_date'].strftime('%d-%m-%Y')
            status = "OVERDUE" if now > info['due_date'] else "Active"
            print(f"{username:<15} {info['book_title']:<30} {borrow:<12} {due:<12} {status:<10}")
        
        print(f"{'='*80}")
    
    def __str__(self) -> str:
        overdue = len(self.get_overdue_books())
        return f"Loans: {len(self._loans)} active, {overdue} overdue"
    
    def __repr__(self) -> str:
        return f"Loans(active={len(self._loans)}, overdue={len(self.get_overdue_books())})"


# test
if __name__ == "__main__":
    # set up test data
    book_list = BookList()
    book1 = Books("Python Programming", "John Smith", 2023, "Tech Books Ltd", 3, "15-06-2023")
    book2 = Books("Data Science Fundamentals", "Jane Doe", 2022, "Academic Press", 2, "20-03-2022")
    book_list.add_book(book1)
    book_list.add_book(book2)
    
    user_list = UserList()
    user1 = Users("jsmith01", "John", "Smith", "14", "Donegall Square West, Belfast", 
                  "BT1 6JS", "john.smith@email.com", "15-05-1990")
    user2 = Users("jdoe02", "Jane", "Doe", "22", "Shipquay Street, Derry",
                  "BT48 6DL", "jane.doe@email.com", "22-08-1985")
    user_list.add_user(user1)
    user_list.add_user(user2)
    
    loans = Loans(book_list, user_list, loan_period_days=14)
    
    print("\n--- Testing Loans ---")
    
    # borrow some books
    print("\nBorrowing books:")
    try:
        loans.borrow_book("jsmith01", book1.get_book_id())
        loans.borrow_book("jdoe02", book1.get_book_id())
        loans.borrow_book("jdoe02", book2.get_book_id())
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
    
    loans.display_all_loans()
    
    print(f"\njsmith01 has {loans.count_user_loans('jsmith01')} book(s)")
    print(f"jdoe02 has {loans.count_user_loans('jdoe02')} book(s)")
    print(f"Available copies of '{book1.get_title()}': {book1.get_available_copies()}")
    
    # return a book
    print("\nReturning book:")
    try:
        loans.return_book("jsmith01", book1.get_book_id())
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
    
    loans.display_all_loans()
    loans.print_overdue_books()
    print(f"\nStatus: {loans}")
