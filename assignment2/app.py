import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import datetime
import os, json

# Import UI modules
from ui_main_menu import *  
from ui_health_log import *
from ui_bmi_calorie import *
from ui_history import *
from ui_profile import *
from ui_login import *
from utils_data import *
from auth import * 


class HealthWellnessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏥 Health & Wellness Assistant")
        self.root.geometry("1000x700")
        
        self.setup_styles()
        
        self.auth = auth_system
        
        self.show_login_screen()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        self.colors = {
            'primary': '#3a86ff',
            'secondary': '#8338ec',
            'success': '#06d6a0',
            'warning': '#ffd166',
            'danger': '#ef476f',
            'dark_bg': '#0f1b2d',
            'card_bg': '#1f2b3e',
            'light_card': '#2a3648',
            'text_light': '#ffffff',
            'text_muted': '#8b9bb4'
        }
        
        style.configure('Primary.TButton',
                        background=self.colors['primary'],
                        foreground='white',
                        padding=(20, 12),
                        font=('Arial', 11, 'bold'))
        
        style.configure('Secondary.TButton',
                        background=self.colors['secondary'],
                        foreground='white',
                        padding=(20, 12),
                        font=('Arial', 11))
        
    # Clear current interface
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Show login screen
    def show_login_screen(self):
        self.clear_frame()
        create_login_screen(self)

    # Show main menu
    def show_main_menu(self):
        if not self.auth.is_logged_in():
            self.show_login_screen()
            return
        
        self.clear_frame()
        create_main_menu(self)

    # Show health log
    def show_health_log(self):
        if not self.auth.is_logged_in():
            self.show_login_screen()
            return
        
        daily_health_log(self)

    # Show BMI calculator
    def show_bmi_calorie(self):
        if not self.auth.is_logged_in():
            self.show_login_screen()
            return
        
        bmi_calorie_calculator(self)

    # Show history records
    def show_history(self):
        if not self.auth.is_logged_in():
            self.show_login_screen()
            return
        
        view_health_history(self)

    # Show user profile
    def show_profile_tab(self, parent):
        if not self.auth.is_logged_in():
            self.show_login_screen()
            return
        
        create_profile_tab(self, parent)

    # Custom logout confirmation dialog
    def custom_logout_confirmation(self):
        """Custom logout confirmation dialog"""
        from tkinter import Toplevel, Label, Button, Frame
    
        # Create dialog window
        dialog = Toplevel(self.root)
        dialog.title("⚠️ Confirm Logout")
        dialog.geometry("500x350")
        dialog.configure(bg=self.colors['dark_bg'])
        dialog.resizable(False, False)
        dialog.transient(self.root)  # Set as child window of main window
        dialog.grab_set()  # Modal dialog
    
        # Center the dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
    
        # Title section
        title_frame = Frame(dialog, bg=self.colors['dark_bg'])
        title_frame.pack(fill='x', pady=(20, 10), padx=20)
    
        Label(title_frame, text="🚪 Logout", 
              font=("Arial", 20, "bold"),
              bg=self.colors['dark_bg'], fg=self.colors['danger']).pack()
    
        Label(title_frame, text="Are you sure you want to logout?",
              font=("Arial", 14),
              bg=self.colors['dark_bg'], fg='white').pack(pady=(5, 0))
    
        # Content area
        content_frame = Frame(dialog, bg=self.colors['card_bg'], 
                             padx=20, pady=15)
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
        # Information messages
        messages = [
            "✅ Your data is saved automatically",
            "🔒 Your session will be secured",
            "↩️ You can login again anytime",
            "💾 No data will be lost"
        ]
    
        for message in messages:
            Label(content_frame, text=message,
                  font=("Arial", 11),
                  bg=self.colors['card_bg'], fg='white',
                  anchor='w').pack(fill='x', pady=3)
    
        # Button area
        button_frame = Frame(dialog, bg=self.colors['dark_bg'])
        button_frame.pack(fill='x', pady=(0, 20), padx=20)
    
        result = {'confirmed': False}  # Use dictionary to allow modification in closure
     
        def on_confirm():
            result['confirmed'] = True
            dialog.destroy()
    
        def on_cancel():
            result['confirmed'] = False
            dialog.destroy()
    
        # Confirm button
        confirm_btn = Button(button_frame, text="✅ Yes, Logout", 
                            bg=self.colors['danger'], fg='white',
                            font=("Arial", 12, "bold"),
                            padx=20, pady=10,
                            command=on_confirm)
        confirm_btn.pack(side='right', padx=(10, 0))
    
        # Cancel button
        cancel_btn = Button(button_frame, text="❌ Cancel", 
                           bg=self.colors['secondary'], fg='white',
                           font=("Arial", 12),
                           padx=20, pady=10,
                           command=on_cancel)
        cancel_btn.pack(side='right')
    
        # Bind ESC key to cancel
        dialog.bind('<Escape>', lambda e: on_cancel())
    
        # Wait for dialog to close
        self.root.wait_window(dialog)
    
        return result['confirmed']

    # Modified logout method using custom dialog
    def logout(self):
        """User logout"""
        # Use custom confirmation dialog
        if not self.custom_logout_confirmation():
            return False  # User cancelled
    
        self.auth.logout()
    
        # Show logout success message
        messagebox.showinfo("👋 Goodbye", 
                           "You have been logged out successfully!")
    
        self.show_login_screen()
        return True
    
    
    def save_all_data(self):
        return True
    
    # Exit application
    def exit_app(self):
        self.root.quit()

    
    @property
    # Get current user profile
    def user_profile(self):
        return self.auth.get_user_profile()
    
    @property
    # Get current user health data
    def health_data(self):
        return self.auth.get_user_health_data()
    
    @property
    # Get current user BMI history
    def bmi_history(self):
        return self.auth.get_user_bmi_history()
    
    # Save user profile
    def save_profile(self, profile_data):
        return self.auth.update_user_profile(profile_data)
    
    # Add health data
    def add_health_data(self, date, data):
        return self.auth.add_health_data(date, data)
    
    # Add BMI record
    def add_bmi_record(self, bmi_data):
        return self.auth.add_bmi_record(bmi_data)
    
    # Get current username
    def get_current_user(self):
        return self.auth.get_current_user()