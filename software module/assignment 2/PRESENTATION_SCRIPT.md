# Library Record System - Presentation Script

## Assignment 2 - Software Development Module

---

## TIMING OVERVIEW (~7.5 Minutes)

| Section | Duration | Cumulative |
|---------|----------|------------|
| Introduction | 0:20 | 0:20 |
| System Architecture & Classes | 1:15 | 1:35 |
| User Interface Overview | 0:25 | 2:00 |
| Book Management Demo | 1:20 | 3:20 |
| User Management Demo | 1:00 | 4:20 |
| Loan Management Demo | 1:15 | 5:35 |
| Reports & Statistics | 0:25 | 6:00 |
| Error Handling Demo | 0:45 | 6:45 |
| Conclusion | 0:15 | 7:00 |

---

## SECTION 1: INTRODUCTION (0:20)

> **This section:** Welcome and project overview.

### Script:
> "Welcome to my demonstration of the Library Record System for Assignment 2. This Python application manages books, users, and loans using object-oriented programming with five main classes. Let me walk you through the system."

---

## SECTION 2: SYSTEM ARCHITECTURE & CLASSES (1:15)

> **This section uses examples of:** Books class with validation, encapsulation (private attributes), type hints, Users class with email validation, Loans class constructor.

### Script:

**[Show file structure]**
> "The system has five modules: `main.py` for the interface, `books.py` and `booklist.py` for book management, `users.py` and `userlist.py` for user management, and `loans.py` for the borrowing system."

**[Show books.py - Lines 16-50]**
> "Here's the Books class with auto-generated ID, title, author, year, publisher, and copies. The constructor uses setters for validation."

**[Highlight books.py - Lines 31, 41, 58]**
> "Notice the underscore prefix on attributes like `_title` and `_book_id` - this is **encapsulation**. Attributes are private and accessed through getters and setters."

**[Show books.py - Lines 22-23]**
> "The code uses **type hints** - `title: str`, `year: int` - this is modern Python best practice."

**[Show users.py - Lines 93-102]**
> "The Users class validates email with regex and ensures date of birth format is correct."

**[Show loans.py - Lines 19-46]**
> "The Loans class takes BookList and UserList references to validate operations. Default loan period is 14 days."

---

## SECTION 3: USER INTERFACE OVERVIEW (0:25)

> **This section uses examples of:** Main menu display and input helper methods.

### Script:

**[Run: python main.py]**
> "Here's the main menu with Book Management, User Management, Loan Management, and Reports options."

**[Show main.py - Lines 66-75 and 123-144]**
> "The menu methods create formatted displays, and helper methods like `get_input` and `get_int_input` handle validation."

---

## SECTION 4: BOOK MANAGEMENT DEMO (1:20)

> **This section uses examples of:** Sample Irish authors (Joyce, Wilde, Stoker), adding a book with auto-generated ID, searching by author, modifying and removing books.

### Script:

**[Select Book Management, then View All Books]**
> "The system has ten pre-loaded books by famous Irish authors - James Joyce, Oscar Wilde, Bram Stoker, Seamus Heaney, and Samuel Beckett."

**[Add a New Book]**
> "Adding a new book - enter the details and it receives an auto-generated ID in format BK- followed by 8 random characters."

**[Search Books by author]**
> "Searching by author 'Joyce' finds both 'Ulysses' and 'Dubliners' using case-insensitive partial matching."

**[Show booklist.py - Lines 41-71]**
> "The search method converts values to lowercase for case-insensitive matching."

**[Modify then Remove a Book]**
> "I can modify book details and remove books with confirmation prompts to prevent accidental deletion."

---

## SECTION 5: USER MANAGEMENT DEMO (1:00)

> **This section uses examples of:** Users with NI addresses, adding a user, duplicate firstname warning when removing.

### Script:

**[View All Users]**
> "Pre-loaded users have Northern Ireland addresses - Belfast, Derry, and Newry."

**[Add a New User]**
> "Adding a user - the postcode is automatically converted to uppercase."

**[Try to Remove by firstname with duplicates]**
> "When removing by first name, if multiple users share that name, the system warns and displays all matches."

**[Show userlist.py - Lines 82-88]**
> "This warning suggests using username removal instead for accuracy - a specific assignment requirement."

---

## SECTION 6: LOAN MANAGEMENT DEMO (1:15)

> **This section uses examples of:** Borrowing a book, 14-day due date calculation, viewing loans, returning a book with availability update.

### Script:

**[Borrow a Book]**
> "Borrowing a book shows available books and users. The due date is automatically calculated as 14 days from today."

**[Show loans.py - Lines 48-100]**
> "The borrow method validates user exists, book exists, copies available, and prevents duplicate borrowing."

**[View User Loans and All Active Loans]**
> "I can view a user's loans or all active loans with due dates and overdue status."

**[Return a Book]**
> "Returning a book increments available copies. If overdue, the system calculates days late."

**[Show loans.py - Lines 131-138]**
> "Here's the overdue check in the return method."

---

## SECTION 7: REPORTS & STATISTICS (0:25)

> **This section uses examples of:** Library statistics and overdue books report.

### Script:

**[View Statistics]**
> "Statistics show total books, total users, active loans, and overdue count."

**[View Overdue Books]**
> "The overdue report shows book title, username, first name, and days overdue."

---

## SECTION 8: ERROR HANDLING DEMO (0:45)

> **This section uses examples of:** Invalid menu choice, empty field, wrong date format, invalid email, duplicate borrow prevention.

### Script:

**[Invalid menu choice]**
> "Entering an invalid choice like '9' prompts for a valid number."

**[Empty title and invalid date]**
> "Empty fields are rejected, and dates must be DD-MM-YYYY format."

**[Invalid email and duplicate borrow]**
> "Invalid emails are rejected. Trying to borrow the same book twice shows 'User already has this book'."

**[Show main.py - Lines 170-176]**
> "All operations use try-except blocks for user-friendly error messages."

---

## SECTION 9: CONCLUSION (0:15)

### Script:
> "In conclusion, this Library Record System demonstrates object-oriented design, full CRUD functionality, robust loan management, and comprehensive error handling. Thank you for watching."

---

## QUICK REFERENCE - LINE NUMBERS

| File | Lines | Content |
|------|-------|---------|
| `main.py` | 29-48 | Sample books (Irish authors) |
| `main.py` | 66-75 | Main menu display |
| `main.py` | 123-144 | Input helper methods |
| `main.py` | 170-176 | Try-except blocks |
| `main.py` | 543-551 | Statistics method |
| `books.py` | 16-50 | Books class constructor |
| `books.py` | 22-23 | Type hints |
| `books.py` | 31, 41, 58 | Private attributes |
| `booklist.py` | 41-71 | Search method |
| `users.py` | 93-102 | Email validation |
| `userlist.py` | 82-88 | Duplicate firstname warning |
| `loans.py` | 19-46 | Loans constructor |
| `loans.py` | 48-100 | Borrow method |
| `loans.py` | 131-138 | Overdue check |

---

## CHECKLIST FOR FULL MARKS

✅ Clear view of user interface  
✅ Clear view of source code for UI  
✅ Clear view of different classes  
✅ Different input types (strings, integers, dates, emails)  
✅ Error handling demonstrated  
✅ Coherent and logical structure  
✅ OOP principles (encapsulation, type hints)  
✅ Under 10 minutes (~7 minutes)  

---

Good luck!
