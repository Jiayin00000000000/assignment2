import json
import os
import hashlib
from datetime import datetime

class AuthenticationSystem:
    def __init__(self):
        self.current_user = None
        self.users_file = "users.json"
        self.load_users()
    
    # Load user data
    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
            self.save_users()
    
    # Save data
    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)
    
    # Password encryption
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    # Register user
    def register(self, username, password, email="", age="", height="", weight=""):
        if username in self.users:
            return False, "Username already exists!"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters!"
        
        # Create user profile
        user_profile = {
            "username": username,
            "password_hash": self.hash_password(password),
            "email": email,
            "profile": {
                "age": age,
                "height": height,
                "weight": weight,
                "gender": "male",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "last_login": ""
            },
            "health_data": {},
            "bmi_history": []
        }
        
        self.users[username] = user_profile
        self.save_users()
        return True, "Registration successful!"
    
    def login(self, username, password):
        """User login"""
        if username not in self.users:
            return False, "Username not found!"
        
        user = self.users[username]
        if user["password_hash"] != self.hash_password(password):
            return False, "Incorrect password!"
        
        # Update last login time
        user["profile"]["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_users()
        
        self.current_user = username
        return True, f"Welcome back, {username}!"
    
    def logout(self):
        """User logout"""
        self.current_user = None
    
    def is_logged_in(self):
        """Check if user is logged in"""
        return self.current_user is not None
    
    def get_current_user(self):
        """Get current user"""
        return self.current_user
    
    def get_user_profile(self, username=None):
        """Get user profile"""
        if username is None:
            username = self.current_user
        
        if username in self.users:
            return self.users[username]["profile"]
        return {}
    
    def get_user_health_data(self, username=None):
        """Get user health data"""
        if username is None:
            username = self.current_user
        
        if username in self.users:
            return self.users[username]["health_data"]
        return {}
    
    def get_user_bmi_history(self, username=None):
        """Get user BMI history"""
        if username is None:
            username = self.current_user
        
        if username in self.users:
            return self.users[username]["bmi_history"]
        return []
    
    def update_user_profile(self, profile_data, username=None):
        """Update user profile"""
        if username is None:
            username = self.current_user
        
        if username in self.users:
            self.users[username]["profile"].update(profile_data)
            self.save_users()
            return True
        return False
    
    def add_health_data(self, date, data, username=None):
        """Add health data"""
        if username is None:
            username = self.current_user
        
        if username in self.users:
            if "health_data" not in self.users[username]:
                self.users[username]["health_data"] = {}
            
            self.users[username]["health_data"][date] = data
            self.save_users()
            return True
        return False
    
    def add_bmi_record(self, bmi_data, username=None):
        """Add BMI record"""
        if username is None:
            username = self.current_user
        
        if username in self.users:
            if "bmi_history" not in self.users[username]:
                self.users[username]["bmi_history"] = []
            
            bmi_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.users[username]["bmi_history"].append(bmi_data)
            
            # Keep only last 10 records
            if len(self.users[username]["bmi_history"]) > 10:
                self.users[username]["bmi_history"] = self.users[username]["bmi_history"][-10:]
            
            self.save_users()
            return True
        return False
    
    def get_all_users(self):
        """Get all users (admin function)"""
        return list(self.users.keys())

# Global authentication instance
auth_system = AuthenticationSystem()