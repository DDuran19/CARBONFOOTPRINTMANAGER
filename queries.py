import json

class UserAuthentication:
    def __init__(self, filename="users.json"):
        self.filename = filename
        self.users_data = self.load_users_data()

    def load_users_data(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is empty, return an empty list
            return []

    def save_users_data(self):
        with open(self.filename, "w") as file:
            json.dump(self.users_data, file, indent=4)

    def login(self, username, password):
        for user in self.users_data:
            if user["username"] == username and user["password"] == password:
                return True
        return False

    def register(self, username, password):
        if not any(user["username"] == username for user in self.users_data):
            new_user = {"username": username, "password": password}
            self.users_data.append(new_user)
            self.save_users_data()
            return True
        return False
    
    def change_password(self, username, old_password, new_password):
        for user in self.users_data:
            if user["username"] == username and user["password"] == old_password:
                user["password"] = new_password
                self.save_users_data()
                return True
        return False

# Example usage:
if __name__ == "__main__":
    auth = UserAuthentication()

    # Register new users
    auth.register("user1", "password1")
    auth.register("user2", "password2")

    # Test login functionality
    print(auth.login("user1", "password1"))  # Output: True
    print(auth.login("user1", "wrong_password"))  # Output: False
    print(auth.login("user3", "password3"))  # Output: False

    # Attempt to register an existing username
    print(auth.register("user2", "password3"))  # Output: False
    
    # Attempt to change password with wrong old password
    print(auth.change_password("user1", "wrong_password", "newerpassword"))  # Output: False
