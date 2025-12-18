import tkinter as tk
from tkinter import messagebox

def create_profile_tab(app, parent):
    colors = app.colors
    
    frame = tk.Frame(parent, bg=colors['dark_bg'])
    frame.pack(fill='both', expand=True)
    
    tk.Label(frame, text="👤 Profile Information",
             font=("Arial", 24, "bold"),
             bg=colors['dark_bg'], fg='white').pack(pady=40)
    
    # Get user information
    current_user = app.auth.get_current_user()
    user_profile = app.user_profile
    
    # Information card
    info_card = tk.Frame(frame, bg=colors['card_bg'], 
                        padx=30, pady=30, relief='raised', borderwidth=2)
    info_card.pack(padx=50, pady=10)
    
    # Title
    tk.Label(info_card, text="📋 Your Current Profile",
             font=("Arial", 18, "bold"),
             bg=colors['card_bg'], fg='#3a86ff').pack(anchor='w', pady=(0, 20))
    
    # Basic information
    info_text = f"""Username: {current_user}
Name: {user_profile.get('name', 'Not set')}
Email: {user_profile.get('email', 'Not set')}
Age: {user_profile.get('age', 'Not set')}
Height: {user_profile.get('height', 'Not set')} cm
Weight: {user_profile.get('weight', 'Not set')} kg
Gender: {user_profile.get('gender', 'Not set').title()}
"""
    
    tk.Label(info_card, text=info_text,
             font=("Arial", 12),
             bg=colors['card_bg'], fg='white',
             justify='left').pack(anchor='w', pady=(0, 20))
    
    # Tip information
    tk.Label(info_card, text="💡 To edit your profile, click the '👤 Profile' button on the main menu.",
             font=("Arial", 10),
             bg=colors['card_bg'], fg='#FFD700').pack(anchor='w')