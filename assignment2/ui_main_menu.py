import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk

def create_main_menu(app):
    try:
        app.clear_frame()
        root = app.root
        colors = app.colors
        
        # Create main frame
        main_frame = tk.Frame(root, bg=colors['dark_bg'])
        main_frame.pack(fill="both", expand=True)
        
        # Top user information bar
        top_bar = tk.Frame(main_frame, bg=colors['card_bg'], height=60)
        top_bar.pack(fill='x', pady=(10, 20), padx=20)
        top_bar.pack_propagate(False)
        
        # Display current user
        current_user = app.auth.get_current_user()
        if current_user:
            user_label = tk.Label(top_bar, text=f"👤 {current_user}", 
                                 font=("Arial", 14, "bold"),
                                 bg=colors['card_bg'], fg='#FFD700')
            user_label.pack(side='left', padx=20)
        else:
            user_label = tk.Label(top_bar, text="👤 Not Logged In", 
                                 font=("Arial", 14),
                                 bg=colors['card_bg'], fg='white')
            user_label.pack(side='left', padx=20)
        
        # Logout button
        logout_btn = tk.Button(top_bar, text="🚪 Logout", 
                              command=app.logout,
                              bg=colors['danger'], fg='white',
                              font=("Arial", 10, "bold"),
                              padx=15, pady=5)
        logout_btn.pack(side='right', padx=20)
        
        # Content container - fill remaining space
        content_frame = tk.Frame(main_frame, bg=colors['dark_bg'])
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Title
        title = tk.Label(
            content_frame,
            text="💪 Health & Wellness Assistant",
            font=("Arial", 32, "bold"),
            bg=colors['dark_bg'],
            fg=colors['text_light']
        )
        title.pack(pady=(0, 40))
        
        menu_items = [
            ("🥗", "Daily Log", app.show_health_log, "#ecbf38"),
            ("🧮", "BMI Calculator", app.show_bmi_calorie, "#faea7a"),
            ("📈", "History", app.show_history, "#aecc73"),
            ("👤", "Profile", lambda: show_edit_profile(app), "#76e4b1"), 
            ("📊", "Reports", lambda: show_reports(app), "#9FD1FF"),
            ("❌", "Exit", app.exit_app, "#ba92eb")
        ]
        
        # Create grid container - fill entire content area
        grid_frame = tk.Frame(content_frame, bg=colors['dark_bg'])
        grid_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Configure grid - 3 rows, 2 columns, evenly distribute space
        for i in range(3):
            grid_frame.grid_rowconfigure(i, weight=1, uniform="rows")
        for i in range(2):
            grid_frame.grid_columnconfigure(i, weight=1, uniform="cols")
        
        def hover_enter(border_frame, icon_label, text_label):
            border_frame.config(highlightbackground="white")
            icon_label.config(fg="white")
            text_label.config(fg="white")
        
        def hover_leave(border_frame, icon_label, text_label, border_color):
            border_frame.config(highlightbackground=border_color)
            icon_label.config(fg="white")
            text_label.config(fg="white")
        
        # Store references to all cards
        menu_cards = []
        
        # Create menu cards
        for index, (icon, text, callback, border_color) in enumerate(menu_items):
            row = index // 2  
            col = index % 2   
            
            # Create menu item container - fill entire grid cell
            item_container = tk.Frame(grid_frame, bg=colors['dark_bg'])
            item_container.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            # Colored border - fill entire container
            border_frame = tk.Frame(
                item_container,
                bg=colors['dark_bg'],
                highlightthickness=4,
                highlightbackground=border_color,
                highlightcolor=border_color
            )
            border_frame.pack(fill="both", expand=True)
            
            # Card - fill entire border
            card = tk.Frame(
                border_frame,
                bg=colors['card_bg'],
                padx=20, pady=20
            )
            card.pack(fill="both", expand=True)
            
            # Card content container - for centering content
            card_content = tk.Frame(card, bg=colors['card_bg'])
            card_content.pack(expand=True, fill="both")
            
            # Large emoji icon
            icon_label = tk.Label(
                card_content,
                text=icon,
                font=("Arial", 50),
                bg=colors['card_bg'],
                fg="white"
            )
            icon_label.pack(expand=True, pady=(10, 5))
            
            # Text
            text_label = tk.Label(
                card_content,
                text=text,
                font=("Arial", 20, "bold"),
                bg=colors['card_bg'],
                fg="white"
            )
            text_label.pack(pady=(0, 10))
            
            # Click event
            def make_callback(cb):
                return lambda e: cb()
            
            click_callback = make_callback(callback)
            
            for w in (border_frame, card, card_content, icon_label, text_label):
                w.bind("<Button-1>", click_callback)
                w.config(cursor="hand2")
            
            # Hover effect
            for w in (border_frame, card, card_content, icon_label, text_label):
                w.bind("<Enter>",
                       lambda e, b=border_frame, i=icon_label, t=text_label: hover_enter(b, i, t))
                
                w.bind("<Leave>",
                       lambda e, b=border_frame, i=icon_label, t=text_label, bc=border_color:
                       hover_leave(b, i, t, bc))
            
            # Store card reference for resizing
            menu_cards.append({
                'container': item_container,
                'border': border_frame,
                'card': card,
                'content': card_content,
                'icon': icon_label,
                'text': text_label,
                'border_color': border_color
            })
        
        # Add bottom spacing
        bottom_spacer = tk.Frame(content_frame, bg=colors['dark_bg'], height=20)
        bottom_spacer.pack(fill='x')
        
        # Function to dynamically adjust card content sizes
        def adjust_card_sizes(event=None):
            """Adjust card content based on window size"""
            if not menu_cards:
                return
            
            # Get first card container size as reference
            container_width = menu_cards[0]['container'].winfo_width()
            container_height = menu_cards[0]['container'].winfo_height()
            
            if container_width > 50 and container_height > 50:  # Ensure container has sufficient size
                # Calculate appropriate font sizes
                icon_size = max(min(container_height // 6, 80), 30)  # emoji size, min 30, max 80
                text_size = max(min(container_height // 15, 24), 14)  # text size, min 14, max 24
                
                for card_info in menu_cards:
                    # Adjust emoji size
                    card_info['icon'].config(font=("Arial", icon_size))
                    
                    # Adjust text size
                    card_info['text'].config(font=("Arial", text_size, "bold"))
                    
                    # Adjust card padding
                    padding = max(min(container_width // 20, container_height // 20, 30), 10)
                    card_info['card'].config(padx=padding, pady=padding)
        
        # Bind window resize event
        def on_container_configure(event):
            adjust_card_sizes()
        
        grid_frame.bind("<Configure>", on_container_configure)
        
        # Initial size adjustment
        def initial_adjust():
            adjust_card_sizes()
            # If size not appropriate, adjust again later
            root.after(100, adjust_card_sizes)
            root.after(500, adjust_card_sizes)
        
        root.after(100, initial_adjust)
                
    except Exception as e:
        # If there's an error, show error message
        messagebox.showerror("Error", f"Failed to create main menu: {str(e)}")
        # Try to return to login screen
        app.show_login_screen()

def show_edit_profile(app):
    """Display editable user profile page"""
    # Create edit window
    edit_window = tk.Toplevel(app.root)
    edit_window.title("👤 Edit Profile")
    edit_window.geometry("700x700")
    edit_window.configure(bg=app.colors['dark_bg'])
    
    # Use Canvas for scrolling
    canvas = tk.Canvas(edit_window, bg=app.colors['dark_bg'], highlightthickness=0)
    scrollbar = tk.Scrollbar(edit_window, orient="vertical", command=canvas.yview)
    scrollable = tk.Frame(canvas, bg=app.colors['dark_bg'])
    
    scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Title
    title_frame = tk.Frame(scrollable, bg=app.colors['dark_bg'])
    title_frame.pack(fill='x', pady=20, padx=30)
    
    tk.Label(title_frame, text="👤 Edit Your Profile",
             font=("Arial", 28, "bold"),
             bg=app.colors['dark_bg'], fg='white').pack(side='left')
    
    # User information
    current_user = app.auth.get_current_user()
    tk.Label(title_frame, text=f"👤 {current_user}",
             font=("Arial", 12),
             bg=app.colors['dark_bg'], fg='#FFD700').pack(side='right')
    
    # Main content area
    main_content = tk.Frame(scrollable, bg=app.colors['dark_bg'])
    main_content.pack(fill='both', expand=True, padx=30, pady=10)
    
    # Create edit form
    create_edit_profile_form(app, main_content, edit_window)
    
    # Bind mousewheel event
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    canvas.bind_all("<MouseWheel>", on_mousewheel)
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

def create_edit_profile_form(app, parent, window):
    """Create profile edit form"""
    colors = app.colors
    
    # Get current user profile
    user_profile = app.user_profile
    
    # Create card
    card = tk.Frame(parent, bg=colors['card_bg'], 
                   padx=30, pady=30, relief='raised', borderwidth=2)
    card.pack(fill='both', expand=True)
    
    # Title
    tk.Label(card, text="📋 Personal Information",
             font=("Arial", 20, "bold"),
             bg=colors['card_bg'], fg='#3a86ff').pack(anchor='w', pady=(0, 25))
    
    # Create StringVar variables with initial values
    profile_age = tk.StringVar(value=str(user_profile.get('age', '')))
    profile_height = tk.StringVar(value=str(user_profile.get('height', '')))
    profile_weight = tk.StringVar(value=str(user_profile.get('weight', '')))
    profile_gender = tk.StringVar(value=user_profile.get('gender', 'male'))
    profile_email = tk.StringVar(value=user_profile.get('email', ''))
    profile_name = tk.StringVar(value=user_profile.get('name', ''))
    
    # Name (optional)
    name_frame = tk.Frame(card, bg=colors['card_bg'])
    name_frame.pack(fill='x', pady=(0, 15))
    tk.Label(name_frame, text="Full Name (Optional)", 
             bg=colors['card_bg'], fg='white', font=("Arial", 12)).pack(anchor='w')
    name_entry = tk.Entry(name_frame, textvariable=profile_name, 
                         bg=colors['light_card'], fg='white',
                         font=("Arial", 12))
    name_entry.pack(fill='x', pady=(5, 0), ipady=8)
    
    # Email (optional)
    email_frame = tk.Frame(card, bg=colors['card_bg'])
    email_frame.pack(fill='x', pady=(0, 15))
    tk.Label(email_frame, text="Email (Optional)", 
             bg=colors['card_bg'], fg='white', font=("Arial", 12)).pack(anchor='w')
    email_entry = tk.Entry(email_frame, textvariable=profile_email, 
                          bg=colors['light_card'], fg='white',
                          font=("Arial", 12))
    email_entry.pack(fill='x', pady=(5, 0), ipady=8)
    
    # Age
    age_frame = tk.Frame(card, bg=colors['card_bg'])
    age_frame.pack(fill='x', pady=(0, 15))
    tk.Label(age_frame, text="Age*", 
             bg=colors['card_bg'], fg='white', font=("Arial", 12, "bold")).pack(anchor='w')
    age_entry = tk.Entry(age_frame, textvariable=profile_age, 
                        bg=colors['light_card'], fg='white',
                        font=("Arial", 14))
    age_entry.pack(fill='x', pady=(5, 0), ipady=8)
    
    # Age tip
    tk.Label(age_frame, text="Required for BMI and calorie calculations",
             bg=colors['card_bg'], fg='#8b9bb4', font=("Arial", 9)).pack(anchor='w', pady=(2, 0))
    
    # Height
    height_frame = tk.Frame(card, bg=colors['card_bg'])
    height_frame.pack(fill='x', pady=(0, 15))
    tk.Label(height_frame, text="Height (cm)*", 
             bg=colors['card_bg'], fg='white', font=("Arial", 12, "bold")).pack(anchor='w')
    height_entry = tk.Entry(height_frame, textvariable=profile_height, 
                           bg=colors['light_card'], fg='white',
                           font=("Arial", 14))
    height_entry.pack(fill='x', pady=(5, 0), ipady=8)
    
    # Height tip
    tk.Label(height_frame, text="Example: 170.5",
             bg=colors['card_bg'], fg='#8b9bb4', font=("Arial", 9)).pack(anchor='w', pady=(2, 0))
    
    # Weight
    weight_frame = tk.Frame(card, bg=colors['card_bg'])
    weight_frame.pack(fill='x', pady=(0, 15))
    tk.Label(weight_frame, text="Weight (kg)*", 
             bg=colors['card_bg'], fg='white', font=("Arial", 12, "bold")).pack(anchor='w')
    weight_entry = tk.Entry(weight_frame, textvariable=profile_weight, 
                           bg=colors['light_card'], fg='white',
                           font=("Arial", 14))
    weight_entry.pack(fill='x', pady=(5, 0), ipady=8)
    
    # Weight tip
    tk.Label(weight_frame, text="Example: 65.2",
             bg=colors['card_bg'], fg='#8b9bb4', font=("Arial", 9)).pack(anchor='w', pady=(2, 0))
    
    # Gender selection - improved version
    gender_frame = tk.Frame(card, bg=colors['card_bg'])
    gender_frame.pack(fill='x', pady=(0, 25))
    tk.Label(gender_frame, text="Gender*", 
             bg=colors['card_bg'], fg='white', font=("Arial", 12, "bold")).pack(anchor='w')
    
    # Custom radio button frame
    gender_btn_frame = tk.Frame(gender_frame, bg=colors['card_bg'])
    gender_btn_frame.pack(fill='x', pady=(8, 0))
    
    # Gender options - using large emoji and custom styles
    gender_options = [
        {"emoji": "👨", "text": "Male", "value": "male", "color": "#4FC3F7"},
        {"emoji": "👩", "text": "Female", "value": "female", "color": "#F06292"},
        {"emoji": "⚧", "text": "Other", "value": "other", "color": "#BA68C8"}
    ]
    
    # Store button references
    gender_buttons = []
    
    # Create custom radio buttons
    for i, option in enumerate(gender_options):
        btn_container = tk.Frame(gender_btn_frame, bg=colors['card_bg'])
        btn_container.pack(side='left', padx=(0, 30) if i < 2 else (0, 0))
        
        # Create clickable frame
        clickable_frame = tk.Frame(btn_container, bg=colors['card_bg'], 
                                  relief='flat', borderwidth=2, cursor="hand2")
        clickable_frame.pack()
        
        # Large emoji label
        emoji_label = tk.Label(clickable_frame, 
                              text=option["emoji"],
                              font=("Arial", 32, "bold"),
                              bg=colors['card_bg'],
                              fg='white')
        emoji_label.pack()
        
        # Text label
        text_label = tk.Label(clickable_frame, 
                             text=option["text"],
                             font=("Arial", 12),
                             bg=colors['card_bg'],
                             fg='white')
        text_label.pack(pady=(5, 8))
        
        # Circular selection indicator
        indicator = tk.Label(clickable_frame, 
                            text="●",
                            font=("Arial", 16),
                            bg=colors['card_bg'],
                            fg=colors['card_bg'])  # Initially transparent
        indicator.pack()
        
        # Store button information
        gender_buttons.append({
            "frame": clickable_frame,
            "emoji": emoji_label,
            "text": text_label,
            "indicator": indicator,
            "value": option["value"],
            "color": option["color"],
            "selected": False
        })
        
        # Bind click event
        for widget in [clickable_frame, emoji_label, text_label, indicator]:
            widget.bind("<Button-1>", lambda e, v=option["value"]: select_gender(v))
    
    # Gender selection functions
    def select_gender(value):
        profile_gender.set(value)
        update_gender_display()
    
    def update_gender_display():
        selected_value = profile_gender.get()
        
        for btn in gender_buttons:
            if btn["value"] == selected_value:
                # Selected state
                btn["frame"].config(bg=btn["color"], relief='sunken')
                btn["emoji"].config(bg=btn["color"], font=("Arial", 36, "bold"))
                btn["text"].config(bg=btn["color"], font=("Arial", 12, "bold"), fg='white')
                btn["indicator"].config(bg=btn["color"], fg='white')
                btn["selected"] = True
            else:
                # Unselected state
                btn["frame"].config(bg=colors['card_bg'], relief='flat')
                btn["emoji"].config(bg=colors['card_bg'], font=("Arial", 32))
                btn["text"].config(bg=colors['card_bg'], font=("Arial", 12), fg='white')
                btn["indicator"].config(bg=colors['card_bg'], fg=colors['card_bg'])
                btn["selected"] = False
    
    # Initialize display
    update_gender_display()
    
    # Add hover effects
    def on_gender_hover(event, button_info):
        """Mouse hover effect"""
        if not button_info["selected"]:
            # Find correct button
            for btn in gender_buttons:
                if btn["value"] == button_info["value"]:
                    btn["frame"].config(bg=btn["color"])
                    btn["emoji"].config(bg=btn["color"])
                    btn["text"].config(bg=btn["color"])
                    btn["indicator"].config(bg=btn["color"])
                    break
    
    def on_gender_leave(event, button_info):
        """Mouse leave effect"""
        if not button_info["selected"]:
            # Find correct button
            for btn in gender_buttons:
                if btn["value"] == button_info["value"]:
                    btn["frame"].config(bg=colors['card_bg'])
                    btn["emoji"].config(bg=colors['card_bg'])
                    btn["text"].config(bg=colors['card_bg'])
                    btn["indicator"].config(bg=colors['card_bg'])
                    break
    
    # Add hover effect to each button
    for btn in gender_buttons:
        for widget in [btn["frame"], btn["emoji"], btn["text"], btn["indicator"]]:
            widget.bind("<Enter>", lambda e, b=btn: on_gender_hover(e, b))
            widget.bind("<Leave>", lambda e, b=btn: on_gender_leave(e, b))
    
    # Button frame
    btn_frame = tk.Frame(card, bg=colors['card_bg'])
    btn_frame.pack(fill='x', pady=(20, 0))
    
    # Save function
    def save_profile():
        """Save user profile"""
        try:
            # Validate required fields
            age_str = profile_age.get().strip()
            height_str = profile_height.get().strip()
            weight_str = profile_weight.get().strip()
            
            if not age_str or not height_str or not weight_str:
                messagebox.showerror("❌ Error", "Please fill in all required fields (age, height, weight)!")
                return
            
            age = int(age_str)
            height = float(height_str)
            weight = float(weight_str)
            
            # Validate reasonableness
            if age < 1 or age > 120:
                messagebox.showerror("❌ Error", "Please enter a valid age (1-120)!")
                return
            
            if height < 50 or height > 250:
                messagebox.showerror("❌ Error", "Please enter a valid height (50-250 cm)!")
                return
            
            if weight < 20 or weight > 300:
                messagebox.showerror("❌ Error", "Please enter a valid weight (20-300 kg)!")
                return
            
            # Prepare profile data
            profile_data = {
                "age": age,
                "height": height,
                "weight": weight,
                "gender": profile_gender.get(),
                "email": profile_email.get().strip(),
                "name": profile_name.get().strip()
            }
            
            # Save using auth system
            success = app.save_profile(profile_data)
            
            if success:
                messagebox.showinfo("✅ Success", "Profile updated successfully!\n\nYour data will be used for BMI and calorie calculations.")
                window.destroy()  # Close edit window
            else:
                messagebox.showerror("❌ Error", "Failed to save profile!")
                
        except ValueError:
            messagebox.showerror("❌ Error", "Please enter valid numbers for age, height, and weight!")
        except Exception as e:
            messagebox.showerror("❌ Error", f"An error occurred: {str(e)}")
    
    # Reset function
    def reset_profile():
        """Reset to current profile data"""
        profile = app.user_profile
        
        profile_age.set(str(profile.get('age', '')))
        profile_height.set(str(profile.get('height', '')))
        profile_weight.set(str(profile.get('weight', '')))
        profile_gender.set(profile.get('gender', 'male'))
        profile_email.set(profile.get('email', ''))
        profile_name.set(profile.get('name', ''))
        
        # Update gender display
        update_gender_display()
        
        messagebox.showinfo("🔄 Reset", "Form reset to current profile data.")
    
    # Save button
    save_btn = tk.Button(btn_frame, text="💾 Save Profile", 
                        bg='#4CAF50', fg='white',
                        font=("Arial", 14, "bold"),
                        padx=30, pady=12,
                        command=save_profile)
    save_btn.pack(side='left', padx=(0, 15))
    
    # Reset button
    reset_btn = tk.Button(btn_frame, text="🔄 Reset to Current",
                         bg=colors['secondary'], fg='white',
                         font=("Arial", 14),
                         padx=20, pady=12,
                         command=reset_profile)
    reset_btn.pack(side='left')
    
    # Close button
    close_btn = tk.Button(btn_frame, text="❌ Cancel",
                         bg=colors['danger'], fg='white',
                         font=("Arial", 14),
                         padx=20, pady=12,
                         command=window.destroy)
    close_btn.pack(side='right')
    
    # Add hover effects
    def on_enter(e, btn):
        btn.config(cursor='hand2')
    
    def on_leave(e, btn):
        btn.config(cursor='')
    
    save_btn.bind("<Enter>", lambda e: on_enter(e, save_btn))
    save_btn.bind("<Leave>", lambda e: on_leave(e, save_btn))
    reset_btn.bind("<Enter>", lambda e: on_enter(e, reset_btn))
    reset_btn.bind("<Leave>", lambda e: on_leave(e, reset_btn))
    close_btn.bind("<Enter>", lambda e: on_enter(e, close_btn))
    close_btn.bind("<Leave>", lambda e: on_leave(e, close_btn))

def show_reports(app):
    """Display health reports page"""
    if not app.auth.is_logged_in():
        messagebox.showerror("❌ Error", "Please login first!")
        app.show_login_screen()
        return
    
    # Create reports window
    report_window = tk.Toplevel(app.root)
    report_window.title("📊 Health Reports")
    report_window.geometry("800x700")
    report_window.configure(bg=app.colors['dark_bg'])
    
    # Title
    title_frame = tk.Frame(report_window, bg=app.colors['dark_bg'])
    title_frame.pack(fill='x', pady=20, padx=30)
    
    tk.Label(title_frame, text="📊 Health Reports & Analytics",
             font=("Arial", 28, "bold"),
             bg=app.colors['dark_bg'], fg='white').pack(side='left')
    
    # User information
    current_user = app.auth.get_current_user()
    tk.Label(title_frame, text=f"👤 {current_user}",
             font=("Arial", 12),
             bg=app.colors['dark_bg'], fg='#FFD700').pack(side='right')
    
    # Create Notebook (tabs)
    notebook = ttk.Notebook(report_window)  # Using ttk.Notebook
    notebook.pack(fill='both', expand=True, padx=20, pady=10)
    
    # Tab 1: Overview
    overview_tab = tk.Frame(notebook, bg=app.colors['dark_bg'])
    notebook.add(overview_tab, text="📈 Overview")
    
    # Tab 2: Recommendations
    recommendations_tab = tk.Frame(notebook, bg=app.colors['dark_bg'])
    notebook.add(recommendations_tab, text="💡 Recommendations")
    
    # Fill overview tab
    fill_overview_tab(app, overview_tab)
    
    # Fill recommendations tab
    fill_recommendations_tab(app, recommendations_tab)
    
    # Close button
    close_frame = tk.Frame(report_window, bg=app.colors['dark_bg'])
    close_frame.pack(fill='x', pady=20)
    
    close_btn = tk.Button(close_frame, text="Close Report",
                         bg=app.colors['secondary'], fg='white',
                         font=("Arial", 12, "bold"),
                         padx=30, pady=10,
                         command=report_window.destroy)
    close_btn.pack()

def fill_overview_tab(app, parent):
    """Fill overview tab"""
    health_data = app.health_data
    
    if not health_data:
        tk.Label(parent, text="No health data available yet.",
                 font=("Arial", 14),
                 bg=app.colors['dark_bg'], fg='white').pack(pady=50)
        return
    
    # Use Canvas for scrolling
    canvas = tk.Canvas(parent, bg=app.colors['dark_bg'], highlightthickness=0)
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollable = tk.Frame(canvas, bg=app.colors['dark_bg'])
    
    scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Calculate statistics
    total_days = len(health_data)
    recent_days = min(7, total_days)
    
    # Get last 7 days data
    sorted_dates = sorted(health_data.keys(), reverse=True)
    recent_data = [health_data[date] for date in sorted_dates[:recent_days]]
    
    # Calculate averages
    if recent_data:
        avg_sleep = sum(d.get('sleep', 0) for d in recent_data) / len(recent_data)
        avg_water = sum(d.get('water', 0) for d in recent_data) / len(recent_data)
        avg_mood = sum(d.get('mood', 0) for d in recent_data) / len(recent_data)
    else:
        avg_sleep = avg_water = avg_mood = 0
    
    # Create cards container
    cards_frame = tk.Frame(scrollable, bg=app.colors['dark_bg'])
    cards_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Statistics card 1: Overall statistics
    stats_card1 = tk.Frame(cards_frame, bg=app.colors['card_bg'],
                          padx=20, pady=20, relief='raised', borderwidth=2)
    stats_card1.pack(fill='x', pady=(0, 15))
    
    tk.Label(stats_card1, text="📅 Overall Statistics",
             font=("Arial", 18, "bold"),
             bg=app.colors['card_bg'], fg='#3a86ff').pack(anchor='w', pady=(0, 15))
    
    overall_text = f"""• Total Logged Days: {total_days}
• Recent Activity (7 days): {recent_days} days
• Average Sleep (Recent): {avg_sleep:.1f} hours
• Average Water (Recent): {avg_water:.1f} cups
• Average Mood (Recent): {avg_mood:.1f}/5
"""
    
    tk.Label(stats_card1, text=overall_text,
             font=("Arial", 12),
             bg=app.colors['card_bg'], fg='white',
             justify='left').pack(anchor='w')
    
    # Statistics card 2: Health score
    health_score = calculate_health_score(avg_sleep, avg_water, avg_mood)
    
    stats_card2 = tk.Frame(cards_frame, bg=app.colors['card_bg'],
                          padx=20, pady=20, relief='raised', borderwidth=2)
    stats_card2.pack(fill='x', pady=(0, 15))
    
    tk.Label(stats_card2, text="⭐ Health Score",
             font=("Arial", 18, "bold"),
             bg=app.colors['card_bg'], fg='#FFD700').pack(anchor='w', pady=(0, 15))
    
    # Health score display
    score_color = '#06d6a0' if health_score >= 70 else ('#FFD166' if health_score >= 50 else '#ef476f')
    tk.Label(stats_card2, text=f"{health_score}/100",
             font=("Arial", 36, "bold"),
             bg=app.colors['card_bg'], fg=score_color).pack(pady=10)
    
    # Score explanation
    if health_score >= 80:
        feedback = "Excellent! Keep up the great work! 💪"
    elif health_score >= 60:
        feedback = "Good! There's room for improvement. 🌟"
    else:
        feedback = "Needs improvement. Focus on consistency! 📈"
    
    tk.Label(stats_card2, text=feedback,
             font=("Arial", 12),
             bg=app.colors['card_bg'], fg='white').pack(pady=10)
    
    # Recent records
    if recent_data:
        recent_card = tk.Frame(cards_frame, bg=app.colors['card_bg'],
                              padx=20, pady=20, relief='raised', borderwidth=2)
        recent_card.pack(fill='x', pady=(0, 15))
        
        tk.Label(recent_card, text="📋 Recent Logs",
                 font=("Arial", 18, "bold"),
                 bg=app.colors['card_bg'], fg='#06d6a0').pack(anchor='w', pady=(0, 15))
        
        # Display last 3 days records
        for i, date in enumerate(sorted_dates[:3]):
            if i >= len(sorted_dates):
                break
                
            data = health_data[date]
            mood_emojis = ["😢", "😕", "😐", "😊", "😄"]
            mood_emoji = mood_emojis[data.get('mood', 3)-1] if 1 <= data.get('mood', 3) <= 5 else "😐"
            
            log_text = f"📅 {date}: Sleep {data.get('sleep', '--')}h • Water {data.get('water', '--')}cups • Mood {mood_emoji}"
            
            log_frame = tk.Frame(recent_card, bg=app.colors['light_card'],
                                padx=10, pady=8)
            log_frame.pack(fill='x', pady=5)
            
            tk.Label(log_frame, text=log_text,
                     font=("Arial", 11),
                     bg=app.colors['light_card'], fg='white').pack(anchor='w')

def fill_recommendations_tab(app, parent):
    """Fill recommendations tab"""
    health_data = app.health_data
    
    if not health_data:
        tk.Label(parent, text="Log more data to get personalized recommendations.",
                 font=("Arial", 14),
                 bg=app.colors['dark_bg'], fg='white').pack(pady=50)
        return
    
    # Calculate recent data
    sorted_dates = sorted(health_data.keys(), reverse=True)
    recent_data = [health_data[date] for date in sorted_dates[:7] if date in health_data]
    
    if not recent_data:
        tk.Label(parent, text="Not enough recent data for recommendations.",
                 font=("Arial", 14),
                 bg=app.colors['dark_bg'], fg='white').pack(pady=50)
        return
    
    # Use Canvas for scrolling
    canvas = tk.Canvas(parent, bg=app.colors['dark_bg'], highlightthickness=0)
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollable = tk.Frame(canvas, bg=app.colors['dark_bg'])
    
    scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Analyze data
    avg_sleep = sum(d.get('sleep', 0) for d in recent_data) / len(recent_data)
    avg_water = sum(d.get('water', 0) for d in recent_data) / len(recent_data)
    avg_mood = sum(d.get('mood', 0) for d in recent_data) / len(recent_data)
    
    # Create recommendations cards
    cards_frame = tk.Frame(scrollable, bg=app.colors['dark_bg'])
    cards_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Sleep recommendations
    sleep_card = tk.Frame(cards_frame, bg=app.colors['card_bg'],
                         padx=20, pady=20, relief='raised', borderwidth=2)
    sleep_card.pack(fill='x', pady=(0, 15))
    
    tk.Label(sleep_card, text="💤 Sleep Recommendations",
             font=("Arial", 18, "bold"),
             bg=app.colors['card_bg'], fg='#4CC9F0').pack(anchor='w', pady=(0, 15))
    
    if avg_sleep < 7:
        sleep_advice = f"""Your average sleep is {avg_sleep:.1f} hours, which is below the recommended 7-9 hours.

🔸 Recommendations:
• Try to go to bed 30 minutes earlier
• Avoid screens 1 hour before bedtime
• Create a relaxing bedtime routine
• Keep your bedroom dark and cool"""
    elif avg_sleep > 9:
        sleep_advice = f"""Your average sleep is {avg_sleep:.1f} hours, which is above the recommended range.

🔸 Recommendations:
• Maintain consistent wake-up times
• Ensure quality over quantity of sleep
• Consult a doctor if consistently sleeping >9 hours"""
    else:
        sleep_advice = f"""Great! Your average sleep is {avg_sleep:.1f} hours, within the healthy range.

🔸 Keep it up:
• Maintain your current sleep schedule
• Continue good sleep hygiene practices"""
    
    tk.Label(sleep_card, text=sleep_advice,
             font=("Arial", 12),
             bg=app.colors['card_bg'], fg='white',
             justify='left', wraplength=600).pack(anchor='w')
    
    # Water recommendations
    water_card = tk.Frame(cards_frame, bg=app.colors['card_bg'],
                         padx=20, pady=20, relief='raised', borderwidth=2)
    water_card.pack(fill='x', pady=(0, 15))
    
    tk.Label(water_card, text="💧 Water Intake Recommendations",
             font=("Arial", 18, "bold"),
             bg=app.colors['card_bg'], fg='#4361EE').pack(anchor='w', pady=(0, 15))
    
    if avg_water < 8:
        water_advice = f"""Your average water intake is {avg_water:.1f} cups, below the recommended 8-10 cups.

🔸 Recommendations:
• Drink a glass of water after waking up
• Keep a water bottle with you at all times
• Set reminders to drink water every hour
• Eat water-rich fruits and vegetables"""
    else:
        water_advice = f"""Excellent! Your average water intake is {avg_water:.1f} cups.

🔸 Keep it up:
• Continue your good hydration habits
• Monitor urine color (aim for pale yellow)"""
    
    tk.Label(water_card, text=water_advice,
             font=("Arial", 12),
             bg=app.colors['card_bg'], fg='white',
             justify='left', wraplength=600).pack(anchor='w')
    
    # Mood recommendations
    mood_card = tk.Frame(cards_frame, bg=app.colors['card_bg'],
                        padx=20, pady=20, relief='raised', borderwidth=2)
    mood_card.pack(fill='x', pady=(0, 15))
    
    tk.Label(mood_card, text="😊 Mood Recommendations",
             font=("Arial", 18, "bold"),
             bg=app.colors['card_bg'], fg='#F72585').pack(anchor='w', pady=(0, 15))
    
    if avg_mood < 3:
        mood_advice = f"""Your average mood is {avg_mood:.1f}/5, which could be improved.

🔸 Recommendations:
• Practice daily gratitude journaling
• Spend time outdoors in nature
• Connect with friends and family
• Engage in physical activity you enjoy
• Consider mindfulness or meditation"""
    elif avg_mood < 4:
        mood_advice = f"""Your average mood is {avg_mood:.1f}/5.

🔸 Suggestions for improvement:
• Identify what brings you joy
• Set small, achievable goals
• Practice self-care regularly
• Seek support when needed"""
    else:
        mood_advice = f"""Excellent! Your average mood is {avg_mood:.1f}/5.

🔸 Keep it up:
• Continue activities that make you happy
• Share positivity with others
• Maintain work-life balance"""
    
    tk.Label(mood_card, text=mood_advice,
             font=("Arial", 12),
             bg=app.colors['card_bg'], fg='white',
             justify='left', wraplength=600).pack(anchor='w')

def calculate_health_score(sleep, water, mood):
    """Calculate health score (0-100)"""
    # Sleep score (0-40 points)
    sleep_score = 0
    if sleep >= 7 and sleep <= 9:
        sleep_score = 40  # Ideal range
    elif sleep >= 6 and sleep <= 10:
        sleep_score = 30  # Acceptable range
    elif sleep >= 5 and sleep <= 11:
        sleep_score = 20  # Marginal range
    else:
        sleep_score = 10  # Unhealthy
    
    # Water score (0-30 points)
    water_score = min(water / 10 * 30, 30)  # 10 cups gets 30 points
    
    # Mood score (0-30 points)
    mood_score = (mood / 5) * 30  # 5 points gets 30 points
    
    total_score = sleep_score + water_score + mood_score
    
    # Ensure between 0-100
    return min(max(total_score, 0), 100)