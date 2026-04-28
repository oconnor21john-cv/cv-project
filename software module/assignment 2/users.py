"""
Users Module - Library Record System

Software Development Module - Assignment 2
"""

import re
from datetime import datetime


class Users:
    """
    Represents a library user/member.
    
    Username is set once at creation and can't be modified afterwards.
    Everything else can be updated through setters.
    """
    
    def __init__(self, username: str, firstname: str, surname: str,
                 house_number: str, street_name: str, postcode: str,
                 email_address: str, date_of_birth: str):
        """Create a new user with the given details."""
        # username can only be set once
        self._set_username(username)
        
        # rest use normal setters
        self.set_firstname(firstname)
        self.set_surname(surname)
        self.set_house_number(house_number)
        self.set_street_name(street_name)
        self.set_postcode(postcode)
        self.set_email_address(email_address)
        self.set_date_of_birth(date_of_birth)
    
    def _set_username(self, username: str) -> None:
        """Private method - only called during init."""
        if not isinstance(username, str):
            raise TypeError("Username must be a string")
        if not username.strip():
            raise ValueError("Username cannot be empty")
        # only letters, numbers, underscores allowed
        if not re.match(r'^[a-zA-Z0-9_]+$', username.strip()):
            raise ValueError("Username can only contain letters, numbers, and underscores")
        self._username = username.strip()
    
    # --- Setters ---
    
    def set_firstname(self, firstname: str) -> None:
        if not isinstance(firstname, str):
            raise TypeError("First name must be a string")
        if not firstname.strip():
            raise ValueError("First name cannot be empty")
        # only letters, spaces, hyphens (for names like Mary-Jane)
        if not re.match(r'^[a-zA-Z\s\-]+$', firstname.strip()):
            raise ValueError("First name can only contain letters, spaces, and hyphens")
        self._firstname = firstname.strip()
    
    def set_surname(self, surname: str) -> None:
        if not isinstance(surname, str):
            raise TypeError("Surname must be a string")
        if not surname.strip():
            raise ValueError("Surname cannot be empty")
        if not re.match(r'^[a-zA-Z\s\-]+$', surname.strip()):
            raise ValueError("Surname can only contain letters, spaces, and hyphens")
        self._surname = surname.strip()
    
    def set_house_number(self, house_number: str) -> None:
        """House number as string to allow things like '12A'"""
        if not isinstance(house_number, str):
            raise TypeError("House number must be a string")
        if not house_number.strip():
            raise ValueError("House number cannot be empty")
        self._house_number = house_number.strip()
    
    def set_street_name(self, street_name: str) -> None:
        if not isinstance(street_name, str):
            raise TypeError("Street name must be a string")
        if not street_name.strip():
            raise ValueError("Street name cannot be empty")
        self._street_name = street_name.strip()
    
    def set_postcode(self, postcode: str) -> None:
        if not isinstance(postcode, str):
            raise TypeError("Postcode must be a string")
        if not postcode.strip():
            raise ValueError("Postcode cannot be empty")
        self._postcode = postcode.strip().upper()  # always uppercase
    
    def set_email_address(self, email_address: str) -> None:
        if not isinstance(email_address, str):
            raise TypeError("Email address must be a string")
        if not email_address.strip():
            raise ValueError("Email address cannot be empty")
        # basic email validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email_address.strip()):
            raise ValueError("Invalid email address format")
        self._email_address = email_address.strip().lower()
    
    def set_date_of_birth(self, date_of_birth: str) -> None:
        if not isinstance(date_of_birth, str):
            raise TypeError("Date of birth must be a string")
        try:
            dob = datetime.strptime(date_of_birth, "%d-%m-%Y")
            if dob > datetime.now():
                raise ValueError("Date of birth cannot be in the future")
            self._date_of_birth = date_of_birth
        except ValueError as e:
            if "does not match format" in str(e) or "unconverted data" in str(e):
                raise ValueError("Date of birth must be in DD-MM-YYYY format")
            raise
    
    # --- Getters ---
    
    def get_username(self) -> str:
        return self._username
    
    def get_firstname(self) -> str:
        return self._firstname
    
    def get_surname(self) -> str:
        return self._surname
    
    def get_house_number(self) -> str:
        return self._house_number
    
    def get_street_name(self) -> str:
        return self._street_name
    
    def get_postcode(self) -> str:
        return self._postcode
    
    def get_email_address(self) -> str:
        return self._email_address
    
    def get_date_of_birth(self) -> str:
        return self._date_of_birth
    
    # --- Utility methods ---
    
    def get_full_name(self) -> str:
        return f"{self._firstname} {self._surname}"
    
    def get_full_address(self) -> str:
        return f"{self._house_number} {self._street_name}, {self._postcode}"
    
    def __str__(self) -> str:
        return (f"Username: {self._username}\n"
                f"Name: {self.get_full_name()}\n"
                f"Address: {self.get_full_address()}\n"
                f"Email: {self._email_address}\n"
                f"Date of Birth: {self._date_of_birth}")
    
    def __repr__(self) -> str:
        return f"Users(username='{self._username}', name='{self.get_full_name()}')"


# test it out
if __name__ == "__main__":
    try:
        user = Users(
            username="jsmith01",
            firstname="John",
            surname="Smith",
            house_number="14",
            street_name="Donegall Square West, Belfast",
            postcode="BT1 6JS",
            email_address="john.smith@email.com",
            date_of_birth="15-05-1990"
        )
        print("User created!")
        print(user)
        
        # test updating
        print("\nUpdating name...")
        user.set_firstname("Jonathan")
        print(f"New name: {user.get_full_name()}")
        
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
