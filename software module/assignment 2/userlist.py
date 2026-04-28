"""
UserList Module - manages the collection of library users

Software Development Module - Assignment 2
"""

from users import Users
from typing import Optional, List


class UserList:
    """
    Manages the library's user collection.
    Dict with username as key.
    """
    
    def __init__(self):
        self._users = {}
    
    def add_user(self, user: Users) -> bool:
        """Add a user. Must be Users instance, username must be unique."""
        if not isinstance(user, Users):
            raise TypeError("Only Users instances can be added")
        
        username = user.get_username()
        if username in self._users:
            raise ValueError(f"Username '{username}' already exists")
        
        self._users[username] = user
        return True

    def find_users_by_firstname(self, firstname: str, partial: bool = False):
        """
        Find users by first name (case-insensitive).

        By default this does an exact match. If partial=True, this will return
        any user where the search term is contained within the first name.

        Returns a list of (username, Users) tuples.
        """
        if not isinstance(firstname, str):
            raise TypeError("First name must be a string")
        if not firstname.strip():
            raise ValueError("First name cannot be empty")

        firstname_lower = firstname.lower().strip()
        matches = []
        for username, user in self._users.items():
            user_firstname = user.get_firstname().lower()
            if partial:
                if firstname_lower in user_firstname:
                    matches.append((username, user))
            else:
                if user_firstname == firstname_lower:
                    matches.append((username, user))
        return matches
    
    def remove_user_by_firstname(self, firstname: str) -> bool:
        """
        Remove user by first name.
        
        Important: if multiple users have the same first name, we warn
        about it and list them all (this is required by the assignment spec).
        Then we remove the first match.
        """
        if not isinstance(firstname, str):
            raise TypeError("First name must be a string")
        if not firstname.strip():
            raise ValueError("First name cannot be empty")
        
        matches = self.find_users_by_firstname(firstname)

        if not matches:
            raise ValueError(f"No user with first name '{firstname}' found")
        
        # warn if multiple matches - this is the assignment requirement
        if len(matches) > 1:
            print(f"\n*** WARNING: Found {len(matches)} users with first name '{firstname}' ***")
            print("Users found:")
            for uname, u in matches:
                print(f"  - Username: {uname}, Full Name: {u.get_full_name()}, Email: {u.get_email_address()}")
            print("\nPlease remove by username to avoid deleting the wrong user.")
            raise ValueError("Multiple users share that first name. Use remove_user_by_username().")

        # exactly one match
        username_to_remove, removed = matches[0]
        del self._users[username_to_remove]
        print(f"User '{removed.get_full_name()}' (Username: {username_to_remove}) removed.")
        return True
    
    def remove_user_by_username(self, username: str) -> bool:
        """Remove user by username - more precise than by firstname."""
        if not isinstance(username, str):
            raise TypeError("Username must be a string")
        if not username.strip():
            raise ValueError("Username cannot be empty")
        
        username = username.strip()
        if username not in self._users:
            raise ValueError(f"No user with username '{username}' found")
        
        removed = self._users[username]
        del self._users[username]
        print(f"User '{removed.get_full_name()}' (Username: {username}) removed.")
        return True
    
    def count_users(self) -> int:
        """Return total number of users."""
        return len(self._users)
    
    def get_user_by_username(self, username: str) -> Optional[Users]:
        """Get user by username. Returns None if not found."""
        if not isinstance(username, str):
            raise TypeError("Username must be a string")
        
        username = username.strip()
        if username in self._users:
            return self._users[username]
        else:
            print(f"No user found with username '{username}'")
            return None
    
    def get_all_users(self) -> List[Users]:
        """Return list of all users."""
        return list(self._users.values())
    
    def search_users_by_firstname(self, firstname: str) -> List[Users]:
        """Search users by first name (partial match, case-insensitive)."""
        if not isinstance(firstname, str):
            raise TypeError("First name must be a string")
        
        firstname_lower = firstname.lower().strip()
        results = []
        for user in self._users.values():
            if firstname_lower in user.get_firstname().lower():
                results.append(user)
        return results
    
    def display_all_users(self) -> None:
        """Print all users nicely."""
        if not self._users:
            print("No users in the collection.")
            return
        
        print(f"\n{'='*60}")
        print(f"LIBRARY USER COLLECTION - Total: {len(self._users)} users")
        print(f"{'='*60}")
        
        for i, user in enumerate(self._users.values(), 1):
            print(f"\n--- User {i} ---")
            print(user)
        
        print(f"\n{'='*60}")
    
    def __str__(self) -> str:
        return f"UserList containing {len(self._users)} users"
    
    def __repr__(self) -> str:
        return f"UserList(users={list(self._users.keys())})"


# testing
if __name__ == "__main__":
    user_list = UserList()
    
    try:
        # create some test users - note two Johns to test the warning
        user1 = Users("jsmith01", "John", "Smith", "14", "Donegall Square West, Belfast", 
                      "BT1 6JS", "john.smith@email.com", "15-05-1990")
        user2 = Users("jdoe02", "Jane", "Doe", "22", "Shipquay Street, Derry",
                      "BT48 6DL", "jane.doe@email.com", "22-08-1985")
        user3 = Users("jbrown03", "John", "Brown", "5", "Hill Street, Newry",
                      "BT34 1AE", "john.brown@email.com", "01-12-1992")
        
        user_list.add_user(user1)
        user_list.add_user(user2)
        user_list.add_user(user3)
        
        user_list.display_all_users()
        print(f"\nTotal: {user_list.count_users()}")
        
        # test getting by username
        print("\nGetting user 'jdoe02':")
        u = user_list.get_user_by_username("jdoe02")
        if u:
            print(u)
        
        # removing by firstname will raise if there are duplicates (e.g. 2 Johns)
        print("\nRemoving by first name 'Jane' (unique):")
        user_list.remove_user_by_firstname("Jane")
        
        print(f"\nTotal after removal: {user_list.count_users()}")
        
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
