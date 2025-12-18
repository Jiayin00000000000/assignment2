import tkinter as tk
from tkinter import scrolledtext, messagebox
import datetime

def view_health_history(app):
    """Display health history records"""
    if not app.auth.is_logged_in():
        app.show_login_screen()
        return
    
    app.clear_frame()
    colors = app.colors
    root = app.root

    # ============ Main Frame ============
    main_frame = tk.Frame(root, bg=colors['dark_bg'])
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # ============ Top Navigation Bar ============
    top_bar = tk.Frame(main_frame, bg=colors['dark_bg'], height=70)
    top_bar.pack(fill='x', pady=(0, 20))
    top_bar.pack_propagate(False)
    
    # Back button
    back_btn = tk.Button(top_bar, text="← Back to Main Menu", 
                         command=app.show_main_menu,
                         bg=colors['secondary'], fg='white',
                         font=("Arial", 12, "bold"),
                         padx=20, pady=8)
    back_btn.pack(side='left')
    
    # Title
    title_label = tk.Label(top_bar, text="📊 Health History",
                          font=("Arial", 28, "bold"),
                          bg=colors['dark_bg'], fg='white')
    title_label.pack(side='left', padx=50)
    
    # User information
    current_user = app.auth.get_current_user()
    user_info = tk.Label(top_bar, text=f"👤 {current_user}",
                        font=("Arial", 12, "bold"),
                        bg=colors['dark_bg'], fg='#FFD700')
    user_info.pack(side='right', padx=20)

    # ============ Content Area ============
    content_frame = tk.Frame(main_frame, bg=colors['dark_bg'])
    content_frame.pack(fill='both', expand=True)

    # Get health data
    health_data = app.health_data
    
    print(f"DEBUG [History]: User: {current_user}")
    print(f"DEBUG [History]: Health data type: {type(health_data)}")
    print(f"DEBUG [History]: Health data: {health_data}")
    
    # If no records exist
    if not health_data:
        no_data_frame = tk.Frame(content_frame, bg=colors['dark_bg'], pady=100)
        no_data_frame.pack(fill='both', expand=True)
        
        tk.Label(no_data_frame, text="📭 No Health Records Yet",
                font=("Arial", 24, "bold"),
                bg=colors['dark_bg'], fg='white').pack(pady=(0, 20))
        
        tk.Label(no_data_frame, text="Start tracking your daily health to see your history here.",
                font=("Arial", 14),
                bg=colors['dark_bg'], fg='#8b9bb4').pack(pady=(0, 30))
        
        start_btn = tk.Button(no_data_frame, text="➕ Start Daily Log",
                             bg='#3a86ff', fg='white',
                             font=("Arial", 14, "bold"),
                             padx=30, pady=15,
                             command=app.show_health_log)
        start_btn.pack()
        return

    # Sort dates (newest to oldest)
    sorted_dates = sorted(health_data.keys(), reverse=True)
    print(f"DEBUG [History]: Sorted dates: {sorted_dates}")
    
    # ============ Statistics Card ============
    stats_card = tk.Frame(content_frame, bg=colors['card_bg'],
                         padx=25, pady=25, relief='raised', borderwidth=2)
    stats_card.pack(fill='x', pady=(0, 20))
    
    tk.Label(stats_card, text="📈 Your Health Statistics",
             font=("Arial", 20, "bold"),
             bg=colors['card_bg'], fg='#3a86ff').pack(anchor='w', pady=(0, 15))
    
    # Calculate statistics
    total_days = len(health_data)
    recent_days = min(7, total_days)
    
    # Get last 7 days data
    recent_dates = sorted_dates[:recent_days]
    recent_data = [health_data[date] for date in recent_dates]
    
    # Calculate averages
    if recent_data:
        avg_sleep = sum(float(d.get('sleep', 0)) for d in recent_data) / len(recent_data)
        avg_water = sum(float(d.get('water', 0)) for d in recent_data) / len(recent_data)
        avg_mood = sum(float(d.get('mood', 0)) for d in recent_data) / len(recent_data)
    else:
        avg_sleep = avg_water = avg_mood = 0
    
    # Statistics display
    stats_grid = tk.Frame(stats_card, bg=colors['card_bg'])
    stats_grid.pack(fill='x')
    
    # Create statistic items
    stats_items = [
        ("📅", "Total Days", f"{total_days} days"),
        ("📊", "7-Day Avg Sleep", f"{avg_sleep:.1f} hours"),
        ("💧", "7-Day Avg Water", f"{avg_water:.1f} cups"),
        ("😊", "7-Day Avg Mood", f"{avg_mood:.1f}/5")
    ]
    
    for i, (icon, label, value) in enumerate(stats_items):
        stat_frame = tk.Frame(stats_grid, bg=colors['card_bg'])
        stat_frame.grid(row=0, column=i, padx=10, pady=5, sticky='nsew')
        stats_grid.columnconfigure(i, weight=1)
        
        tk.Label(stat_frame, text=icon,
                font=("Arial", 24),
                bg=colors['card_bg'], fg='white').pack()
        
        tk.Label(stat_frame, text=label,
                font=("Arial", 11),
                bg=colors['card_bg'], fg='#8b9bb4').pack()
        
        tk.Label(stat_frame, text=value,
                font=("Arial", 16, "bold"),
                bg=colors['card_bg'], fg='white').pack()

    # ============ History Records List ============
    history_frame = tk.Frame(content_frame, bg=colors['dark_bg'])
    history_frame.pack(fill='both', expand=True, pady=(20, 0))
    
    tk.Label(history_frame, text=f"📅 Your Daily Logs ({total_days} records)",
             font=("Arial", 20, "bold"),
             bg=colors['dark_bg'], fg='white').pack(anchor='w', pady=(0, 15))
    
    # Create left-right split
    left_frame = tk.Frame(history_frame, bg=colors['dark_bg'])
    left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
    
    right_frame = tk.Frame(history_frame, bg=colors['dark_bg'])
    right_frame.pack(side='right', fill='both', expand=True)
    
    # Left side: Date list
    dates_card = tk.Frame(left_frame, bg=colors['card_bg'],
                         padx=15, pady=15)
    dates_card.pack(fill='both', expand=True)
    
    tk.Label(dates_card, text="Select Date to View",
             font=("Arial", 16, "bold"),
             bg=colors['card_bg'], fg='white').pack(anchor='w', pady=(0, 15))
    
    # Create date list frame
    dates_list_frame = tk.Frame(dates_card, bg=colors['card_bg'])
    dates_list_frame.pack(fill='both', expand=True)
    
    # Add scrollbar
    dates_canvas = tk.Canvas(dates_list_frame, bg=colors['card_bg'], 
                           highlightthickness=0)
    dates_scrollbar = tk.Scrollbar(dates_list_frame, orient="vertical", 
                                 command=dates_canvas.yview)
    dates_scrollable = tk.Frame(dates_canvas, bg=colors['card_bg'])
    
    dates_scrollable.bind(
        "<Configure>",
        lambda e: dates_canvas.configure(scrollregion=dates_canvas.bbox("all"))
    )
    
    dates_canvas.create_window((0, 0), window=dates_scrollable, anchor="nw")
    dates_canvas.configure(yscrollcommand=dates_scrollbar.set)
    
    dates_canvas.pack(side="left", fill="both", expand=True)
    dates_scrollbar.pack(side="right", fill="y")
    
    # Store date button references
    date_buttons = []
    
    # Create date buttons
    for i, date_str in enumerate(sorted_dates):
        date_btn_frame = tk.Frame(dates_scrollable, bg=colors['card_bg'])
        date_btn_frame.pack(fill='x', pady=2)
        
        # Format date display
        try:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            display_date = date_obj.strftime("%b %d, %Y")
            weekday = date_obj.strftime("%A")
        except:
            display_date = date_str
            weekday = ""
        
        # Get data for this date
        data = health_data[date_str]
        sleep_val = data.get('sleep', '--')
        water_val = data.get('water', '--')
        mood_val = data.get('mood', '--')
        
        # Determine icon
        if sleep_val != '--' and water_val != '--' and mood_val != '--':
            icon = "✅"
        else:
            icon = "📝"
        
        # Create date button
        date_btn = tk.Button(date_btn_frame, 
                            text=f"{icon} {display_date}",
                            bg=colors['light_card'], fg='white',
                            font=("Arial", 11),
                            padx=15, pady=10,
                            anchor='w',
                            relief='flat',
                            cursor="hand2")
        date_btn.pack(fill='x')
        
        # Add weekday label
        if weekday:
            weekday_label = tk.Label(date_btn_frame, 
                                    text=weekday,
                                    font=("Arial", 9),
                                    bg=colors['light_card'], 
                                    fg='#8b9bb4',
                                    padx=15)
            weekday_label.pack(fill='x', pady=(0, 5))
        
        # Store date and button reference
        date_info = {
            'date': date_str,
            'button': date_btn,
            'frame': date_btn_frame,
            'selected': False
        }
        date_buttons.append(date_info)
        
        # Bind click event - use closure to avoid lambda variable issues
        def make_callback(date_str=date_str, btn_info=date_info):
            return lambda: show_date_details(date_str, btn_info)
        
        date_btn.config(command=make_callback())
    
    # Right side: Details card
    details_card = tk.Frame(right_frame, bg=colors['card_bg'],
                           padx=25, pady=25, relief='raised', borderwidth=2)
    details_card.pack(fill='both', expand=True)
    
    # Date title frame
    date_title_frame = tk.Frame(details_card, bg=colors['card_bg'])
    date_title_frame.pack(fill='x', pady=(0, 20))
    
    # Store as instance variable for access
    app.history_selected_date_label = tk.Label(date_title_frame, 
                                              text="📅 Select a date to view details",
                                              font=("Arial", 18, "bold"),
                                              bg=colors['card_bg'], fg='white')
    app.history_selected_date_label.pack(side='left')
    
    # Details content
    details_content = tk.Frame(details_card, bg=colors['card_bg'])
    details_content.pack(fill='both', expand=True)
    
    # Create details display area
    app.history_details_text = scrolledtext.ScrolledText(details_content,
                                                        bg=colors['light_card'],
                                                        fg='white',
                                                        font=("Arial", 12),
                                                        wrap='word',
                                                        height=20,
                                                        padx=15, pady=15)
    app.history_details_text.pack(fill='both', expand=True)
    app.history_details_text.config(state='disabled')
    
    def show_date_details(date_str, btn_info=None):
        """Display detailed information for selected date"""
        print(f"DEBUG [History]: Showing details for {date_str}")
        
        # Update all button states
        for date_info in date_buttons:
            if date_info['date'] == date_str:
                # Selected date
                date_info['button'].config(bg='#3a86ff', font=("Arial", 11, "bold"))
                date_info['selected'] = True
                # Update weekday label
                for widget in date_info['frame'].winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.config(bg='#3a86ff')
            else:
                # Unselected date
                date_info['button'].config(bg=colors['light_card'], font=("Arial", 11))
                date_info['selected'] = False
                # Update weekday label
                for widget in date_info['frame'].winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.config(bg=colors['light_card'])
        
        # Get data for this date - directly from health_data
        data = health_data.get(date_str, {})
        print(f"DEBUG [History]: Data for {date_str}: {data}")
        
        # Update title
        try:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            display_date = date_obj.strftime("%B %d, %Y")
            weekday = date_obj.strftime("%A")
            app.history_selected_date_label.config(text=f"📅 {display_date} ({weekday})")
        except:
            app.history_selected_date_label.config(text=f"📅 {date_str}")
        
        # Update details
        app.history_details_text.config(state='normal')
        app.history_details_text.delete("1.0", "end")
        
        if data:
            # Format display
            timestamp = data.get('timestamp', '')
            sleep = data.get('sleep', '--')
            water = data.get('water', '--')
            mood_value = data.get('mood', 3)
            
            # Mood emoji mapping
            mood_emojis = ["😢", "😕", "😐", "😊", "😄"]
            mood_emoji = mood_emojis[mood_value-1] if 1 <= mood_value <= 5 else "😐"
            
            # Build display content
            content = f"📊 Daily Health Summary\n"
            content += f"{'═'*35}\n\n"
            
            content += f"📅 Date: {date_str}\n"
            if timestamp:
                content += f"⏰ Recorded at: {timestamp}\n"
            content += f"\n"
            
            content += f"📈 Health Metrics:\n"
            content += f"{'─'*20}\n"
            content += f"• 💤 Sleep: {sleep} hours\n"
            content += f"• 💧 Water: {water} cups\n"
            content += f"• 😊 Mood: {mood_emoji} ({mood_value}/5)\n"
            content += f"\n"
            
            # Meal records
            meals = data.get('meals', '')
            if meals and meals.strip():
                content += f"🍽️ Meals:\n"
                content += f"{'─'*15}\n"
                content += f"{meals}\n"
                content += f"\n"
            
            # Reflection records
            reflection = data.get('reflection', '')
            if reflection and reflection.strip():
                content += f"📝 Daily Reflection:\n"
                content += f"{'─'*20}\n"
                content += f"{reflection}\n"
            
            # Health advice
            content += f"\n💡 Health Insights:\n"
            content += f"{'─'*20}\n"
            
            # Sleep advice
            try:
                sleep_float = float(sleep)
                if sleep_float < 7:
                    content += f"• Sleep: Below recommended 7-9 hours. Try to sleep more.\n"
                elif sleep_float > 9:
                    content += f"• Sleep: Above recommended range. Maintain consistent schedule.\n"
                else:
                    content += f"• Sleep: Within healthy range! Keep it up.\n"
            except:
                pass
            
            # Water advice
            try:
                water_float = float(water)
                if water_float < 8:
                    content += f"• Water: Below recommended 8 cups. Drink more water.\n"
                else:
                    content += f"• Water: Good hydration! Stay consistent.\n"
            except:
                pass
            
            # Mood advice
            if mood_value < 3:
                content += f"• Mood: Consider activities that boost your mood.\n"
            elif mood_value > 4:
                content += f"• Mood: Great mood! Keep doing what makes you happy.\n"
            
        else:
            content = f"No data recorded for {date_str}\n\n"
            content += f"Click 'Edit This Log' to add data for this date."
        
        app.history_details_text.insert("1.0", content)
        app.history_details_text.config(state='disabled')
        
        # Store currently selected date
        app.selected_history_date = date_str
    
    # Default show first record
    if sorted_dates:
        show_date_details(sorted_dates[0])
    
    # Bind mousewheel events
    def on_mousewheel(event):
        dates_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    dates_canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    # Add extra debug button for testing
    debug_frame = tk.Frame(main_frame, bg=colors['dark_bg'])
    debug_frame.pack(fill='x', pady=(10, 0))
    
    debug_btn = tk.Button(debug_frame, text="🐛 Debug Data",
                         bg='#FF6B6B', fg='white',
                         font=("Arial", 10),
                         padx=10, pady=5,
                         command=lambda: debug_current_data(app, health_data, sorted_dates))
    debug_btn.pack(side='right')

def debug_current_data(app, health_data, sorted_dates):
    """Debug current data"""
    print(f"\n=== DEBUG CURRENT DATA ===")
    print(f"Current user: {app.auth.get_current_user()}")
    print(f"Total health records: {len(health_data)}")
    print(f"Sorted dates: {sorted_dates}")
    
    if health_data:
        print("\nFirst 3 records:")
        for date in sorted_dates[:3]:
            data = health_data[date]
            print(f"  {date}: sleep={data.get('sleep', '--')}, water={data.get('water', '--')}, mood={data.get('mood', '--')}")
    
    # Show in message box
    if health_data:
        dates_str = "\n".join(sorted_dates[:10])
        messagebox.showinfo("Debug Info", 
                           f"Total records: {len(health_data)}\n"
                           f"First 10 dates:\n{dates_str}")
    else:
        messagebox.showinfo("Debug Info", "No health data found!")