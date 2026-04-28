"""
Library Record System - Main

Command interface for managing the library - books, users, and loans.


Software Development Module - Assignment 2
"""

from books import Books
from booklist import BookList
from users import Users
from userlist import UserList
from loans import Loans
from datetime import datetime


class LibrarySystem:
    """
    Main application class. Handles menus and user interaction.
    """
    
    def __init__(self):
        self._book_list = BookList()
        self._user_list = UserList()
        self._loans = Loans(self._book_list, self._user_list)
        self._load_sample_data()
    
    def _load_sample_data(self):
        
        
        try:
            books = [
                Books("Ulysses", "James Joyce", 1922, "Sylvia Beach", 3, "02-02-1922"),
                Books("Dubliners", "James Joyce", 1914, "Grant Richards", 4, "15-06-1914"),
                Books("The Picture of Dorian Gray", "Oscar Wilde", 1890, "Lippincott's Monthly", 2, "20-06-1890"),
                Books("Dracula", "Bram Stoker", 1897, "Archibald Constable", 5, "26-05-1897"),
                Books("Gulliver's Travels", "Jonathan Swift", 1726, "Benjamin Motte", 3, "28-10-1726"),
                Books("Death of a Naturalist", "Seamus Heaney", 1966, "Faber and Faber", 4, "12-05-1966"),
                Books("Waiting for Godot", "Samuel Beckett", 1953, "Les Éditions de Minuit", 2, "05-01-1953"),
                Books("Normal People", "Sally Rooney", 2018, "Faber and Faber", 6, "28-08-2018"),
                Books("The Sea", "John Banville", 2005, "Picador", 3, "01-09-2005"),
                Books("Paddy Clarke Ha Ha Ha", "Roddy Doyle", 1993, "Secker and Warburg", 4, "01-05-1993"),
            ]
            for b in books:
                self._book_list.add_book(b)
        except Exception as e:
            print(f"Error loading sample books: {e}")
        
        # sample users
        try:
            users = [
                Users("jsmith01", "John", "Smith", "14", "Donegall Square West, Belfast", "BT1 6JS", 
                      "john.smith@email.com", "15-05-1990"),
                Users("jdoe02", "Jane", "Doe", "22", "Shipquay Street, Derry", "BT48 6DL",
                      "jane.doe@email.com", "22-08-1985"),
                Users("rbrown03", "Robert", "Brown", "5", "Hill Street, Newry", "BT34 1AE",
                      "robert.brown@email.com", "01-12-1992"),
            ]
            for u in users:
                self._user_list.add_user(u)
        except Exception as e:
            print(f"Error loading sample users: {e}")
    
    def clear_screen(self):
        print("\n" * 2)
    
    # --- Menu displays ---
    
    def display_main_menu(self):
        print("\n" + "="*60)
        print("       LIBRARY RECORD SYSTEM - MAIN MENU")
        print("="*60)
        print("  1. Book Management")
        print("  2. User Management")
        print("  3. Loan Management")
        print("  4. Reports")
        print("  5. Exit")
        print("="*60)
    
    def display_book_menu(self):
        print("\n" + "-"*50)
        print("       BOOK MANAGEMENT")
        print("-"*50)
        print("  1. Add a new book")
        print("  2. Modify a book")
        print("  3. Search for books")
        print("  4. Remove a book")
        print("  5. View all books")
        print("  6. Back to main menu")
        print("-"*50)
    
    def display_user_menu(self):
        print("\n" + "-"*50)
        print("       USER MANAGEMENT")
        print("-"*50)
        print("  1. Add a new user")
        print("  2. Modify a user")
        print("  3. Search for users")
        print("  4. Remove a user")
        print("  5. View all users")
        print("  6. Back to main menu")
        print("-"*50)
    
    def display_loan_menu(self):
        print("\n" + "-"*50)
        print("       LOAN MANAGEMENT")
        print("-"*50)
        print("  1. Borrow a book")
        print("  2. Return a book")
        print("  3. View user's loans")
        print("  4. View all active loans")
        print("  5. Back to main menu")
        print("-"*50)
    
    def display_reports_menu(self):
        print("\n" + "-"*50)
        print("       REPORTS")
        print("-"*50)
        print("  1. View overdue books")
        print("  2. Library statistics")
        print("  3. Back to main menu")
        print("-"*50)
    
    # --- Input helpers ---
    
    def get_input(self, prompt: str, allow_empty: bool = False) -> str:
        """Get string input, optionally requiring non-empty."""
        while True:
            val = input(prompt).strip()
            if val or allow_empty:
                return val
            print("This field cannot be empty. Please try again.")
    
    def get_int_input(self, prompt: str, min_val: int = None, max_val: int = None) -> int:
        """Get integer input with optional range validation."""
        while True:
            try:
                val = int(input(prompt).strip())
                if min_val is not None and val < min_val:
                    print(f"Value must be at least {min_val}")
                    continue
                if max_val is not None and val > max_val:
                    print(f"Value must be at most {max_val}")
                    continue
                return val
            except ValueError:
                print("Please enter a valid number.")
    
    # --- Book operations ---
    
    def add_book(self):
        print("\n--- ADD NEW BOOK ---")
        try:
            title = self.get_input("Enter book title: ")
            author = self.get_input("Enter author name: ")
            year = self.get_int_input("Enter publication year: ", 1000, datetime.now().year)
            publisher = self.get_input("Enter publisher: ")
            num_copies = self.get_int_input("Enter number of copies: ", 1)
            
            # get date with validation
            while True:
                pub_date = self.get_input("Enter publication date (DD-MM-YYYY): ")
                try:
                    datetime.strptime(pub_date, "%d-%m-%Y")
                    break
                except ValueError:
                    print("Invalid date format. Please use DD-MM-YYYY.")
            
            book = Books(title, author, year, publisher, num_copies, pub_date)
            self._book_list.add_book(book)
            print(f"\nSUCCESS: Book '{title}' added with ID: {book.get_book_id()}")
            
        except (ValueError, TypeError) as e:
            print(f"\nERROR: Could not add book - {e}")
    
    def modify_book(self):
        print("\n--- MODIFY BOOK ---")
        self._book_list.display_all_books()
        
        if self._book_list.get_total_books() == 0:
            return
        
        book_id = self.get_input("\nEnter the Book ID to modify: ")
        book = self._book_list.get_book_by_id(book_id)
        
        if book is None:
            print(f"No book found with ID '{book_id}'")
            return
        
        print(f"\nCurrent details for '{book.get_title()}':")
        print(book)
        
        print("\nWhat would you like to modify?")
        print("  1. Title")
        print("  2. Author")
        print("  3. Year")
        print("  4. Publisher")
        print("  5. Number of copies")
        print("  6. Cancel")
        
        choice = self.get_int_input("Enter choice (1-6): ", 1, 6)
        
        try:
            if choice == 1:
                new_val = self.get_input("Enter new title: ")
                book.set_title(new_val)
                print(f"SUCCESS: Title updated to '{new_val}'")
            elif choice == 2:
                new_val = self.get_input("Enter new author: ")
                book.set_author(new_val)
                print(f"SUCCESS: Author updated to '{new_val}'")
            elif choice == 3:
                new_val = self.get_int_input("Enter new year: ", 1000, datetime.now().year)
                book.set_year(new_val)
                print(f"SUCCESS: Year updated to {new_val}")
            elif choice == 4:
                new_val = self.get_input("Enter new publisher: ")
                book.set_publisher(new_val)
                print(f"SUCCESS: Publisher updated to '{new_val}'")
            elif choice == 5:
                new_val = self.get_int_input("Enter new number of copies: ", 0)
                book.set_num_copies(new_val)
                # adjust available if needed
                if book.get_available_copies() > new_val:
                    book.set_available_copies(new_val)
                print(f"SUCCESS: Number of copies updated to {new_val}")
            else:
                print("Modification cancelled.")
        except (ValueError, TypeError) as e:
            print(f"ERROR: Could not modify book - {e}")
    
    def search_books(self):
        print("\n--- SEARCH BOOKS ---")
        print("Search by:")
        print("  1. Title")
        print("  2. Author")
        print("  3. Publisher")
        print("  4. Publication date")
        
        choice = self.get_int_input("Enter choice (1-4): ", 1, 4)
        fields = {1: 'title', 2: 'author', 3: 'publisher', 4: 'publication_date'}
        search_by = fields[choice]
        
        term = self.get_input(f"Enter {search_by} to search: ")
        
        try:
            results = self._book_list.search_book(term, search_by)
            if not results:
                print(f"\nNo books found matching '{term}'")
            else:
                print(f"\nFound {len(results)} book(s):")
                for i, book in enumerate(results, 1):
                    print(f"\n--- Result {i} ---")
                    print(book)
        except (ValueError, TypeError) as e:
            print(f"ERROR: Search failed - {e}")
    
    def remove_book(self):
        print("\n--- REMOVE BOOK ---")
        self._book_list.display_all_books()
        
        if self._book_list.get_total_books() == 0:
            return
        
        title = self.get_input("\nEnter the title of the book to remove: ")
        confirm = self.get_input(f"Are you sure you want to remove '{title}'? (yes/no): ")
        
        if confirm.lower() != 'yes':
            print("Removal cancelled.")
            return
        
        try:
            self._book_list.remove_book(title)
        except (ValueError, TypeError) as e:
            print(f"ERROR: Could not remove book - {e}")
    
    # --- User operations ---
    
    def add_user(self):
        print("\n--- ADD NEW USER ---")
        try:
            username = self.get_input("Enter username (alphanumeric): ")
            firstname = self.get_input("Enter first name: ")
            surname = self.get_input("Enter surname: ")
            house_number = self.get_input("Enter house number: ")
            street_name = self.get_input("Enter street name: ")
            postcode = self.get_input("Enter postcode: ")
            
            # email validation
            while True:
                email = self.get_input("Enter email address: ")
                if '@' in email and '.' in email:
                    break
                print("Invalid email format. Please try again.")
            
            # dob validation
            while True:
                dob = self.get_input("Enter date of birth (DD-MM-YYYY): ")
                try:
                    datetime.strptime(dob, "%d-%m-%Y")
                    break
                except ValueError:
                    print("Invalid date format. Please use DD-MM-YYYY.")
            
            user = Users(username, firstname, surname, house_number, 
                        street_name, postcode, email, dob)
            self._user_list.add_user(user)
            print(f"\nSUCCESS: User '{username}' added!")
            
        except (ValueError, TypeError) as e:
            print(f"\nERROR: Could not add user - {e}")
    
    def modify_user(self):
        print("\n--- MODIFY USER ---")
        self._user_list.display_all_users()
        
        if self._user_list.count_users() == 0:
            return
        
        username = self.get_input("\nEnter the username to modify: ")
        user = self._user_list.get_user_by_username(username)
        
        if user is None:
            print(f"No user found with username '{username}'")
            return
        
        print(f"\nCurrent details for '{username}':")
        print(user)
        
        print("\nWhat would you like to modify?")
        print("  1. First name")
        print("  2. Surname")
        print("  3. House number")
        print("  4. Street name")
        print("  5. Postcode")
        print("  6. Email address")
        print("  7. Date of birth")
        print("  8. Cancel")
        
        choice = self.get_int_input("Enter choice (1-8): ", 1, 8)
        
        try:
            if choice == 1:
                new_val = self.get_input("Enter new first name: ")
                user.set_firstname(new_val)
                print(f"SUCCESS: First name updated to '{new_val}'")
            elif choice == 2:
                new_val = self.get_input("Enter new surname: ")
                user.set_surname(new_val)
                print(f"SUCCESS: Surname updated to '{new_val}'")
            elif choice == 3:
                new_val = self.get_input("Enter new house number: ")
                user.set_house_number(new_val)
                print(f"SUCCESS: House number updated to '{new_val}'")
            elif choice == 4:
                new_val = self.get_input("Enter new street name: ")
                user.set_street_name(new_val)
                print(f"SUCCESS: Street name updated to '{new_val}'")
            elif choice == 5:
                new_val = self.get_input("Enter new postcode: ")
                user.set_postcode(new_val)
                print(f"SUCCESS: Postcode updated to '{new_val}'")
            elif choice == 6:
                new_val = self.get_input("Enter new email address: ")
                user.set_email_address(new_val)
                print(f"SUCCESS: Email updated to '{new_val}'")
            elif choice == 7:
                while True:
                    new_val = self.get_input("Enter new date of birth (DD-MM-YYYY): ")
                    try:
                        datetime.strptime(new_val, "%d-%m-%Y")
                        user.set_date_of_birth(new_val)
                        print(f"SUCCESS: Date of birth updated to '{new_val}'")
                        break
                    except ValueError:
                        print("Invalid date format. Please use DD-MM-YYYY.")
            else:
                print("Modification cancelled.")
        except (ValueError, TypeError) as e:
            print(f"ERROR: Could not modify user - {e}")
    
    def search_users(self):
        print("\n--- SEARCH USERS ---")
        firstname = self.get_input("Enter first name to search: ")
        
        try:
            results = self._user_list.search_users_by_firstname(firstname)
            if not results:
                print(f"\nNo users found with first name containing '{firstname}'")
            else:
                print(f"\nFound {len(results)} user(s):")
                for i, user in enumerate(results, 1):
                    print(f"\n--- Result {i} ---")
                    print(user)
        except (ValueError, TypeError) as e:
            print(f"ERROR: Search failed - {e}")
    
    def remove_user(self):
        print("\n--- REMOVE USER ---")
        self._user_list.display_all_users()
        
        if self._user_list.count_users() == 0:
            return
        
        print("\nRemove by:")
        print("  1. First name")
        print("  2. Username")
        
        choice = self.get_int_input("Enter choice (1-2): ", 1, 2)
        
        try:
            if choice == 1:
                firstname = self.get_input("Enter the first name of the user to remove: ")
                # partial match allowed here (e.g. "jo" -> John)
                matches = self._user_list.find_users_by_firstname(firstname, partial=True)

                if not matches:
                    print(f"No users found with first name '{firstname}'.")
                    return

                # if only one, show details and confirm
                if len(matches) == 1:
                    username, user = matches[0]
                    print("\nUser found:")
                    print(f"Username: {username}")
                    print(user)
                    confirm = self.get_input(f"\nRemove this user? (yes/no): ")
                    if confirm.lower() == "yes":
                        self._user_list.remove_user_by_username(username)
                    else:
                        print("Removal cancelled.")
                    return

                # multiple matches: show numbered options with full details
                print(f"\nFound {len(matches)} users with first name '{firstname}':")
                for i, (username, user) in enumerate(matches, 1):
                    print(f"\nOption {i}:")
                    print(f"Username: {username}")
                    print(user)

                pick = self.get_int_input(
                    f"\nChoose which user to remove (1-{len(matches)}) or 0 to cancel: ",
                    0,
                    len(matches),
                )
                if pick == 0:
                    print("Removal cancelled.")
                    return

                username, user = matches[pick - 1]
                print("\nYou selected:")
                print(f"Username: {username}")
                print(user)
                confirm = self.get_input("\nRemove this user? (yes/no): ")
                if confirm.lower() == "yes":
                    self._user_list.remove_user_by_username(username)
                else:
                    print("Removal cancelled.")
            else:
                username = self.get_input("Enter the username of the user to remove: ")
                confirm = self.get_input(f"Are you sure you want to remove user '{username}'? (yes/no): ")
                if confirm.lower() == 'yes':
                    self._user_list.remove_user_by_username(username)
                else:
                    print("Removal cancelled.")
        except (ValueError, TypeError) as e:
            print(f"ERROR: Could not remove user - {e}")
    
    # --- Loan operations ---
    
    def borrow_book(self):
        print("\n--- BORROW BOOK ---")
        
        # show available books
        print("\nAvailable Books:")
        books = self._book_list.get_all_books()
        available = [b for b in books if b.get_available_copies() > 0]
        
        if not available:
            print("No books available for borrowing.")
            return
        
        for book in available:
            print(f"  ID: {book.get_book_id()} | {book.get_title()} | Available: {book.get_available_copies()}")
        
        # show users
        print("\nRegistered Users:")
        for user in self._user_list.get_all_users():
            print(f"  Username: {user.get_username()} | {user.get_full_name()}")
        
        username = self.get_input("\nEnter username: ")
        book_id = self.get_input("Enter book ID: ")
        
        try:
            self._loans.borrow_book(username, book_id)
        except (ValueError, TypeError) as e:
            print(f"ERROR: Could not borrow book - {e}")
    
    def return_book(self):
        print("\n--- RETURN BOOK ---")
        
        username = self.get_input("Enter username: ")
        
        # show their loans
        loans = self._loans.get_user_loans(username)
        if not loans:
            print(f"User '{username}' has no books to return.")
            return
        
        print(f"\nBooks borrowed by '{username}':")
        for loan in loans:
            status = "OVERDUE" if loan['is_overdue'] else "Active"
            print(f"  ID: {loan['book_id']} | {loan['book_title']} | Due: {loan['due_date'].strftime('%d-%m-%Y')} | {status}")
        
        book_id = self.get_input("\nEnter book ID to return: ")
        
        try:
            self._loans.return_book(username, book_id)
        except (ValueError, TypeError) as e:
            print(f"ERROR: Could not return book - {e}")
    
    def view_user_loans(self):
        print("\n--- VIEW USER LOANS ---")
        
        username = self.get_input("Enter username: ")
        loans = self._loans.get_user_loans(username)
        count = self._loans.count_user_loans(username)
        
        if not loans:
            print(f"\nUser '{username}' has no active loans.")
        else:
            print(f"\n{username} has {count} book(s) borrowed:")
            for loan in loans:
                status = "OVERDUE" if loan['is_overdue'] else "Active"
                print(f"  - {loan['book_title']} | Due: {loan['due_date'].strftime('%d-%m-%Y')} | {status}")
    
    # --- Reports ---
    
    def view_overdue_books(self):
        self._loans.print_overdue_books()
    
    def view_statistics(self):
        print("\n" + "="*50)
        print("       LIBRARY STATISTICS")
        print("="*50)
        print(f"  Total Books:        {self._book_list.get_total_books()}")
        print(f"  Total Users:        {self._user_list.count_users()}")
        print(f"  Active Loans:       {self._loans.get_total_active_loans()}")
        print(f"  Overdue Books:      {len(self._loans.get_overdue_books())}")
        print("="*50)
    
    # --- Menu handlers ---
    
    def handle_book_menu(self):
        while True:
            self.display_book_menu()
            choice = self.get_int_input("Enter choice (1-6): ", 1, 6)
            
            if choice == 1:
                self.add_book()
            elif choice == 2:
                self.modify_book()
            elif choice == 3:
                self.search_books()
            elif choice == 4:
                self.remove_book()
            elif choice == 5:
                self._book_list.display_all_books()
            else:
                break
    
    def handle_user_menu(self):
        while True:
            self.display_user_menu()
            choice = self.get_int_input("Enter choice (1-6): ", 1, 6)
            
            if choice == 1:
                self.add_user()
            elif choice == 2:
                self.modify_user()
            elif choice == 3:
                self.search_users()
            elif choice == 4:
                self.remove_user()
            elif choice == 5:
                self._user_list.display_all_users()
            else:
                break
    
    def handle_loan_menu(self):
        while True:
            self.display_loan_menu()
            choice = self.get_int_input("Enter choice (1-5): ", 1, 5)
            
            if choice == 1:
                self.borrow_book()
            elif choice == 2:
                self.return_book()
            elif choice == 3:
                self.view_user_loans()
            elif choice == 4:
                self._loans.display_all_loans()
            else:
                break
    
    def handle_reports_menu(self):
        while True:
            self.display_reports_menu()
            choice = self.get_int_input("Enter choice (1-3): ", 1, 3)
            
            if choice == 1:
                self.view_overdue_books()
            elif choice == 2:
                self.view_statistics()
            else:
                break
    
    def run(self):
        """Main loop - starts the application."""
        print("\n" + "="*60)
        print("  Welcome to the Library Record System")
        print("  Software Module Assignment 2")
        print("="*60)
        
        while True:
            self.display_main_menu()
            choice = self.get_int_input("Enter choice (1-5): ", 1, 5)
            
            if choice == 1:
                self.handle_book_menu()
            elif choice == 2:
                self.handle_user_menu()
            elif choice == 3:
                self.handle_loan_menu()
            elif choice == 4:
                self.handle_reports_menu()
            else:
                print("\nThank you for using the Library Record System. Goodbye!")
                break


if __name__ == "__main__":
    library = LibrarySystem()
    library.run()
