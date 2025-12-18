import tkinter as tk
from tkinter import messagebox
from auth import auth_system

def create_login_screen(app):
    app.clear_frame()
    colors = app.colors
    
    # Create main frame
    main_frame = tk.Frame(app.root, bg=colors['dark_bg'])
    main_frame.pack(fill='both', expand=True)
    
    # Left welcome area
    left_frame = tk.Frame(main_frame, bg=colors['dark_bg'], width=400)
    left_frame.pack(side='left', fill='both', expand=True)
    
    # Right login area
    right_frame = tk.Frame(main_frame, bg=colors['dark_bg'])
    right_frame.pack(side='right', fill='both', expand=True, padx=50, pady=50)
    
    # === Left welcome content ===
    welcome_frame = tk.Frame(left_frame, bg='#1a237e')
    welcome_frame.pack(fill='both', expand=True, padx=40, pady=40)
    
    # Large emoji and title
    tk.Label(welcome_frame, text="🏥", 
             font=("Arial", 80),
             bg='#1a237e', fg='white').pack(pady=(40, 10))
    
    tk.Label(welcome_frame, text="Health & Wellness", 
             font=("Arial", 36, "bold"),
             bg='#1a237e', fg='white').pack(pady=(0, 10))
    
    tk.Label(welcome_frame, text="Assistant", 
             font=("Arial", 36, "bold"),
             bg='#1a237e', fg='#3a86ff').pack(pady=(0, 30))
    
    # Features list
    features = [
        "📊 Track your daily health metrics",
        "⚖️ Calculate BMI and ideal weight",
        "🔥 Monitor calorie intake and needs",
        "📈 View your health history and trends",
        "💪 Get personalized fitness recommendations"
    ]
    
    for feature in features:
        tk.Label(welcome_frame, text=feature,
                 font=("Arial", 14),
                 bg='#1a237e', fg='#bbdefb',
                 justify='left').pack(anchor='w', pady=8, padx=20)
    
    # === Right login form ===
    login_card = tk.Frame(right_frame, bg=colors['card_bg'], 
                         padx=40, pady=40, relief='raised', borderwidth=2)
    login_card.pack(fill='both', expand=True)
    
    tk.Label(login_card, text="🔐 Welcome Back!", 
             font=("Arial", 28, "bold"),
             bg=colors['card_bg'], fg='white').pack(pady=(0, 40))
    
    # Username
    tk.Label(login_card, text="👤 Username", 
             font=("Arial", 14),
             bg=colors['card_bg'], fg='white').pack(anchor='w', pady=(0, 8))
    
    app.login_username_var = tk.StringVar()
    username_entry = tk.Entry(login_card, textvariable=app.login_username_var,
                             font=("Arial", 16),
                             bg=colors['light_card'], fg='white',
                             width=30)
    username_entry.pack(pady=(0, 20), ipady=10)
    username_entry.focus()
    
    # Password
    tk.Label(login_card, text="🔒 Password", 
             font=("Arial", 14),
             bg=colors['card_bg'], fg='white').pack(anchor='w', pady=(0, 8))
    
    app.login_password_var = tk.StringVar()
    password_entry = tk.Entry(login_card, textvariable=app.login_password_var,
                             font=("Arial", 16),
                             bg=colors['light_card'], fg='white',
                             show="*", width=30)
    password_entry.pack(pady=(0, 30), ipady=10)
    
    # Button frame
    button_frame = tk.Frame(login_card, bg=colors['card_bg'])
    button_frame.pack(fill='x', pady=(0, 20))
    
    # Login button
    login_btn = tk.Button(button_frame, text="🚀 Login", 
                         bg='#3a86ff', fg='white',
                         font=("Arial", 16, "bold"),
                         padx=40, pady=12,
                         command=lambda: perform_login(app))
    login_btn.pack(side='left', padx=(0, 10))
    
    # Exit button - add here
    exit_btn = tk.Button(button_frame, text="❌ Exit", 
                        bg='#ef476f', fg='white',
                        font=("Arial", 16, "bold"),
                        padx=40, pady=12,
                        command=app.exit_app)  # Use app's exit_app method
    exit_btn.pack(side='right')
    
    # Add hover effect to exit button
    def on_exit_enter(e):
        exit_btn.config(bg='#ff6b6b', cursor='hand2')
    
    def on_exit_leave(e):
        exit_btn.config(bg='#ef476f', cursor='')
    
    exit_btn.bind("<Enter>", on_exit_enter)
    exit_btn.bind("<Leave>", on_exit_leave)
    
    # Register button
    register_btn = tk.Button(login_card, text="✨ Create New Account", 
                            bg=colors['secondary'], fg='white',
                            font=("Arial", 14),
                            padx=30, pady=10,
                            command=lambda: show_register_form(app, login_card))
    register_btn.pack(pady=(10, 0))
    
    # Guest mode button
    guest_btn = tk.Button(login_card, text="👤 Continue as Guest", 
                         bg=colors['light_card'], fg='white',
                         font=("Arial", 12),
                         padx=30, pady=8,
                         command=lambda: guest_login(app))
    guest_btn.pack(pady=(20, 0))
    
    # Bind Enter key for login
    username_entry.bind('<Return>', lambda e: perform_login(app))
    password_entry.bind('<Return>', lambda e: perform_login(app))
    
    # Bind ESC key for exit
    app.root.bind('<Escape>', lambda e: app.exit_app())

def show_register_form(app, login_card):
    """Display registration form"""
    # Hide login form
    for widget in login_card.winfo_children():
        widget.pack_forget()
    
    # Create registration form
    tk.Label(login_card, text="✨ Create Account", 
             font=("Arial", 28, "bold"),
             bg=app.colors['card_bg'], fg='white').pack(pady=(0, 30))
    
    # Username
    tk.Label(login_card, text="👤 Choose Username", 
             font=("Arial", 14),
             bg=app.colors['card_bg'], fg='white').pack(anchor='w', pady=(0, 8))
    
    app.register_username_var = tk.StringVar()
    reg_user_entry = tk.Entry(login_card, textvariable=app.register_username_var,
                             font=("Arial", 16),
                             bg=app.colors['light_card'], fg='white',
                             width=30)
    reg_user_entry.pack(pady=(0, 15), ipady=10)
    reg_user_entry.focus()
    
    # Password
    tk.Label(login_card, text="🔒 Create Password", 
             font=("Arial", 14),
             bg=app.colors['card_bg'], fg='white').pack(anchor='w', pady=(0, 8))
    
    app.register_password_var = tk.StringVar()
    reg_pass_entry = tk.Entry(login_card, textvariable=app.register_password_var,
                             font=("Arial", 16),
                             bg=app.colors['light_card'], fg='white',
                             show="*", width=30)
    reg_pass_entry.pack(pady=(0, 15), ipady=10)
    
    # Confirm password
    tk.Label(login_card, text="🔒 Confirm Password", 
             font=("Arial", 14),
             bg=app.colors['card_bg'], fg='white').pack(anchor='w', pady=(0, 8))
    
    app.register_confirm_var = tk.StringVar()
    confirm_entry = tk.Entry(login_card, textvariable=app.register_confirm_var,
                            font=("Arial", 16),
                            bg=app.colors['light_card'], fg='white',
                            show="*", width=30)
    confirm_entry.pack(pady=(0, 30), ipady=10)
    
    # Button frame
    reg_button_frame = tk.Frame(login_card, bg=app.colors['card_bg'])
    reg_button_frame.pack(fill='x', pady=(0, 15))
    
    # Register button
    register_btn = tk.Button(reg_button_frame, text="✅ Register", 
                            bg='#06d6a0', fg='white',
                            font=("Arial", 16, "bold"),
                            padx=40, pady=12,
                            command=lambda: perform_register(app))
    register_btn.pack(side='left', padx=(0, 10))
    
    # Exit button - also add in registration form
    exit_btn = tk.Button(reg_button_frame, text="❌ Exit", 
                        bg='#ef476f', fg='white',
                        font=("Arial", 16, "bold"),
                        padx=40, pady=12,
                        command=app.exit_app)
    exit_btn.pack(side='right')
    
    # Add hover effect
    exit_btn.bind("<Enter>", lambda e: exit_btn.config(bg='#ff6b6b', cursor='hand2'))
    exit_btn.bind("<Leave>", lambda e: exit_btn.config(bg='#ef476f', cursor=''))
    
    # Back to login button
    back_btn = tk.Button(login_card, text="← Back to Login", 
                        bg=app.colors['light_card'], fg='white',
                        font=("Arial", 12),
                        command=lambda: recreate_login_screen(app, login_card))
    back_btn.pack()
    
    # EnteR for registration
    reg_user_entry.bind('<Return>', lambda e: perform_register(app))
    reg_pass_entry.bind('<Return>', lambda e: perform_register(app))
    confirm_entry.bind('<Return>', lambda e: perform_register(app))
    
    # ESC exit
    app.root.bind('<Escape>', lambda e: app.exit_app())

def recreate_login_screen(app, login_card):
    """Recreate login form"""
    # Clear current card
    for widget in login_card.winfo_children():
        widget.destroy()
    
    # Recreate login form
    tk.Label(login_card, text="🔐 Welcome Back!", 
             font=("Arial", 28, "bold"),
             bg=app.colors['card_bg'], fg='white').pack(pady=(0, 40))
    
    tk.Label(login_card, text="👤 Username", 
             font=("Arial", 14),
             bg=app.colors['card_bg'], fg='white').pack(anchor='w', pady=(0, 8))
    
    app.login_username_var = tk.StringVar()
    username_entry = tk.Entry(login_card, textvariable=app.login_username_var,
                             font=("Arial", 16),
                             bg=app.colors['light_card'], fg='white',
                             width=30)
    username_entry.pack(pady=(0, 20), ipady=10)
    
    tk.Label(login_card, text="🔒 Password", 
             font=("Arial", 14),
             bg=app.colors['card_bg'], fg='white').pack(anchor='w', pady=(0, 8))
    
    app.login_password_var = tk.StringVar()
    password_entry = tk.Entry(login_card, textvariable=app.login_password_var,
                             font=("Arial", 16),
                             bg=app.colors['light_card'], fg='white',
                             show="*", width=30)
    password_entry.pack(pady=(0, 30), ipady=10)
    
    # Button frame
    button_frame = tk.Frame(login_card, bg=app.colors['card_bg'])
    button_frame.pack(fill='x', pady=(0, 20))
    
    # Login button
    login_btn = tk.Button(button_frame, text="🚀 Login", 
                         bg='#3a86ff', fg='white',
                         font=("Arial", 16, "bold"),
                         padx=40, pady=12,
                         command=lambda: perform_login(app))
    login_btn.pack(side='left', padx=(0, 10))
    
    # Exit button
    exit_btn = tk.Button(button_frame, text="❌ Exit", 
                        bg='#ef476f', fg='white',
                        font=("Arial", 16, "bold"),
                        padx=40, pady=12,
                        command=app.exit_app)
    exit_btn.pack(side='right')
    
    # Add hover effect
    exit_btn.bind("<Enter>", lambda e: exit_btn.config(bg='#ff6b6b', cursor='hand2'))
    exit_btn.bind("<Leave>", lambda e: exit_btn.config(bg='#ef476f', cursor=''))
    
    register_btn = tk.Button(login_card, text="✨ Create New Account", 
                            bg=app.colors['secondary'], fg='white',
                            font=("Arial", 14),
                            padx=30, pady=10,
                            command=lambda: show_register_form(app, login_card))
    register_btn.pack()

def perform_login(app):
    """Perform login operation"""
    username = app.login_username_var.get()
    password = app.login_password_var.get()
    
    if not username or not password:
        messagebox.showerror("❌ Error", "Please enter username and password!")
        return
    
    success, message = app.auth.login(username, password)
    
    if success:
        messagebox.showinfo("✅ Success", message)
        app.show_main_menu()
    else:
        messagebox.showerror("❌ Login Failed", message)

def perform_register(app):
    """Perform registration operation"""
    username = app.register_username_var.get()
    password = app.register_password_var.get()
    confirm = app.register_confirm_var.get()
    
    if not username or not password:
        messagebox.showerror("❌ Error", "Please fill in all fields!")
        return
    
    if password != confirm:
        messagebox.showerror("❌ Error", "Passwords do not match!")
        return
    
    success, message = app.auth.register(username, password)
    
    if success:
        messagebox.showinfo("✅ Success", message)
        # Auto login
        app.auth.login(username, password)
        app.show_main_menu()
    else:
        messagebox.showerror("❌ Registration Failed", message)

def guest_login(app):
    """Guest mode login"""
    # Create temporary guest account
    import random
    guest_username = f"guest_{random.randint(1000, 9999)}"
    success, _ = app.auth.register(guest_username, "guest123", "Guest User")
    
    if success:
        app.auth.login(guest_username, "guest123")
        messagebox.showinfo("👤 Guest Mode", f"Logged in as {guest_username}\n\nNote: Guest data will not be saved permanently.")
        app.show_main_menu()