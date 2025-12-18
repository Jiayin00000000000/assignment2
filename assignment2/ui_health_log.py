import tkinter as tk
from tkinter import scrolledtext, messagebox
import datetime

def daily_health_log(app):
    """Display daily health log interface"""
    if not app.auth.is_logged_in():
        app.show_login_screen()
        return
    
    app.clear_frame()
    colors = app.colors
    root = app.root

    # Use larger fonts and spacing
    large_font = ("Arial", 14)
    title_font = ("Arial", 24, "bold")
    emoji_font = ("Arial", 28)  # Mood emoji font
    
    # Define vibrant color scheme
    vibrant_colors = {
        'sleep': '#4CC9F0',    # Bright blue
        'water': '#4361EE',    # Dark blue
        'mood': '#F72585',     # Pink
        'meals': '#7209B7',    # Purple
        'reflection': '#3A0CA3', # Dark purple
        'save': '#4CAF50',     # Green
        'card': '#1A1F2C',      # Dark card background
        'today': '#FFD700'      # Gold - today's date
    }
    
    # User information display
    current_user = app.auth.get_current_user()
    user_profile = app.user_profile

    # Use Canvas and Scrollbar for scrolling
    canvas = tk.Canvas(root, bg=colors['dark_bg'], highlightthickness=0)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=colors['dark_bg'])
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ============ Top Navigation Bar ============
    top_bar = tk.Frame(scrollable_frame, bg=colors['dark_bg'], height=70)
    top_bar.pack(fill='x', pady=(10, 20), padx=20)
    top_bar.pack_propagate(False)
    
    # Back button
    back_btn = tk.Button(top_bar, text="← Back to Main Menu", 
                         command=app.show_main_menu,
                         bg=colors['secondary'], fg='white',
                         font=("Arial", 12, "bold"),
                         padx=20, pady=8)
    back_btn.pack(side='left')
    
    # User information
    user_info = tk.Frame(top_bar, bg=colors['dark_bg'])
    user_info.pack(side='right')
    
    tk.Label(user_info, text=f"👤 {current_user}", 
             font=("Arial", 12, "bold"),
             bg=colors['dark_bg'], fg='#FFD700').pack(anchor='e')
    
    # Display basic info if user profile exists
    if user_profile.get('age'):
        profile_text = f"Age: {user_profile.get('age')}"
        if user_profile.get('height'):
            profile_text += f" • Height: {user_profile.get('height')}cm"
        tk.Label(user_info, text=profile_text,
                font=("Arial", 10),
                bg=colors['dark_bg'], fg='#8b9bb4').pack(anchor='e')

    # ============ Main Title Area ============
    title_frame = tk.Frame(scrollable_frame, bg=colors['dark_bg'])
    title_frame.pack(fill='x', pady=(0, 30), padx=20)
    
    # Large calendar emoji
    tk.Label(title_frame, text="📅", 
             font=("Arial", 60),
             bg=colors['dark_bg'], fg=vibrant_colors['today']).pack(side='left', padx=(0, 20))
    
    # Title and date
    title_text_frame = tk.Frame(title_frame, bg=colors['dark_bg'])
    title_text_frame.pack(side='left')
    
    tk.Label(title_text_frame, text="Daily Health Log",
             font=title_font,
             bg=colors['dark_bg'], fg='white').pack(anchor='w')
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    weekday = datetime.datetime.now().strftime("%A")
    tk.Label(title_text_frame, text=f"{today} • {weekday}",
             font=("Arial", 16),
             bg=colors['dark_bg'], fg=vibrant_colors['today']).pack(anchor='w', pady=(5, 0))

    # Load existing data for today
    today_data = app.health_data.get(today, {})
    
    # ============ Main Content Area ============
    main_content = tk.Frame(scrollable_frame, bg=colors['dark_bg'])
    main_content.pack(fill='both', expand=True, padx=20)

    # Left-right split
    left_frame = tk.Frame(main_content, bg=colors['dark_bg'])
    left_frame.pack(side='left', fill='both', expand=True, padx=10)

    right_frame = tk.Frame(main_content, bg=colors['dark_bg'])
    right_frame.pack(side='right', fill='both', expand=True, padx=10)

    # === Left Column: Basic Metrics Input ===
    
    # Sleep input card
    sleep_card = tk.Frame(left_frame, bg=vibrant_colors['card'], 
                         padx=25, pady=25, relief='raised', borderwidth=2)
    sleep_card.pack(fill='x', pady=(0, 15))
    
    tk.Label(sleep_card, text="💤 Sleep Hours", 
             font=("Arial", 18, "bold"),
             bg=vibrant_colors['card'], fg=vibrant_colors['sleep']).pack(anchor='w', pady=(0, 15))
    
    app.sleep_var = tk.StringVar(value=str(today_data.get('sleep', '')))
    sleep_entry = tk.Entry(sleep_card, textvariable=app.sleep_var, 
                          font=large_font,
                          bg=colors['light_card'], fg='white',
                          insertbackground='white',
                          relief='flat', borderwidth=2)
    sleep_entry.pack(fill='x', pady=5, ipady=10)
    
    # Sleep advice label
    sleep_tip = tk.Label(sleep_card, 
                        text="💡 Recommended: 7-9 hours for adults",
                        font=("Arial", 10),
                        bg=vibrant_colors['card'], fg='#8b9bb4')
    sleep_tip.pack(anchor='w', pady=(8, 0))

    # Water intake input card
    water_card = tk.Frame(left_frame, bg=vibrant_colors['card'],
                         padx=25, pady=25, relief='raised', borderwidth=2)
    water_card.pack(fill='x', pady=(0, 15))
    
    tk.Label(water_card, text="💧 Water Intake (cups)", 
             font=("Arial", 18, "bold"),
             bg=vibrant_colors['card'], fg=vibrant_colors['water']).pack(anchor='w', pady=(0, 15))
    
    app.water_var = tk.StringVar(value=str(today_data.get('water', '')))
    water_entry = tk.Entry(water_card, textvariable=app.water_var,
                          font=large_font,
                          bg=colors['light_card'], fg='white',
                          insertbackground='white',
                          relief='flat', borderwidth=2)
    water_entry.pack(fill='x', pady=5, ipady=10)
    
    # Water intake advice
    water_tip = tk.Label(water_card, 
                        text="💡 Recommended: 8-10 cups daily",
                        font=("Arial", 10),
                        bg=vibrant_colors['card'], fg='#8b9bb4')
    water_tip.pack(anchor='w', pady=(8, 0))

    # Mood selection card - extra large emoji version
    mood_card = tk.Frame(left_frame, bg=vibrant_colors['card'],
                        padx=25, pady=25, relief='raised', borderwidth=2)
    mood_card.pack(fill='x', pady=(0, 15))
    
    tk.Label(mood_card, text="😊 Today's Mood", 
             font=("Arial", 18, "bold"),
             bg=vibrant_colors['card'], fg=vibrant_colors['mood']).pack(anchor='w', pady=(0, 15))
    
    app.mood_var = tk.IntVar(value=today_data.get('mood', 3))
    
    # Create mood selection grid
    moods_grid = tk.Frame(mood_card, bg=vibrant_colors['card'])
    moods_grid.pack()
    
    # Mood options - extra large emoji
    mood_options = [
        ("😢", "Very Sad", 1, "#FF6B6B"),
        ("😕", "Sad", 2, "#FFA726"),
        ("😐", "Neutral", 3, "#FFD166"),
        ("😊", "Happy", 4, "#06D6A0"),
        ("😄", "Very Happy", 5, "#4CC9F0")
    ]
    
    # Create custom mood selection buttons
    mood_buttons = []
    
    for emoji, text, value, color in mood_options:
        mood_btn_frame = tk.Frame(moods_grid, bg=vibrant_colors['card'], 
                                 relief='flat', borderwidth=2)
        mood_btn_frame.pack(side='left', padx=8, pady=5)
        
        # Create emoji label (actual clickable area)
        emoji_label = tk.Label(mood_btn_frame, 
                              text=emoji,
                              font=emoji_font,
                              bg=vibrant_colors['card'],
                              cursor="hand2")
        
        # Create text label
        text_label = tk.Label(mood_btn_frame, 
                             text=text,
                             font=("Arial", 10),
                             bg=vibrant_colors['card'], 
                             fg='white',
                             cursor="hand2")
        
        # Layout
        emoji_label.pack()
        text_label.pack()
        
        # Store references
        mood_info = {
            'frame': mood_btn_frame,
            'emoji': emoji_label,
            'text': text_label,
            'value': value,
            'color': color,
            'selected': False
        }
        mood_buttons.append(mood_info)
        
        # Bind click events
        for widget in [mood_btn_frame, emoji_label, text_label]:
            widget.bind("<Button-1>", lambda e, v=value: select_mood(v))
            widget.bind("<Enter>", lambda e, c=color: on_mood_hover(c, e.widget.master if hasattr(e.widget, 'master') else e.widget))
            widget.bind("<Leave>", lambda e: on_mood_leave())
    
    # Mood selection functions
    def select_mood(value):
        app.mood_var.set(value)
        update_mood_display()
    
    def update_mood_display():
        selected_value = app.mood_var.get()
        for mood in mood_buttons:
            if mood['value'] == selected_value:
                # Selected mood
                mood['frame'].config(bg=mood['color'], relief='sunken')
                mood['emoji'].config(bg=mood['color'], font=(emoji_font[0], emoji_font[1] + 4, "bold"))
                mood['text'].config(bg=mood['color'], font=("Arial", 10, "bold"))
                mood['selected'] = True
            else:
                # Unselected mood
                mood['frame'].config(bg=vibrant_colors['card'], relief='flat')
                mood['emoji'].config(bg=vibrant_colors['card'], font=emoji_font)
                mood['text'].config(bg=vibrant_colors['card'], font=("Arial", 10))
                mood['selected'] = False
    
    def on_mood_hover(color, widget):
        if not any(m['selected'] for m in mood_buttons if m['frame'] == widget):
            widget.config(bg=color)
            for child in widget.winfo_children():
                child.config(bg=color)
    
    def on_mood_leave():
        update_mood_display()
    
    # Initialize mood display
    update_mood_display()

    # === Right Column: Text Record Areas ===
    
    # Meal record card
    meals_card = tk.Frame(right_frame, bg=vibrant_colors['card'],
                         padx=25, pady=25, relief='raised', borderwidth=2)
    meals_card.pack(fill='both', expand=True, pady=(0, 15))
    
    tk.Label(meals_card, text="🍽️ Today's Meals", 
             font=("Arial", 18, "bold"),
             bg=vibrant_colors['card'], fg=vibrant_colors['meals']).pack(anchor='w', pady=(0, 15))
    
    # Example text
    meals_example = """Breakfast: Oatmeal with fruits
Lunch: Chicken salad with vegetables
Dinner: Grilled fish with brown rice
Snacks: Apple, yogurt, nuts"""
    
    app.meals_text = scrolledtext.ScrolledText(meals_card, 
                                              font=("Arial", 12),
                                              bg=colors['light_card'], fg='white',
                                              wrap='word',
                                              height=10,
                                              padx=15, pady=15,
                                              insertbackground='white')
    app.meals_text.pack(fill='both', expand=True)
    
    # Insert existing data or example
    existing_meals = today_data.get('meals', '')
    if existing_meals:
        app.meals_text.insert("1.0", existing_meals)
    else:
        app.meals_text.insert("1.0", meals_example)
    
    # Reflection record card
    reflection_card = tk.Frame(right_frame, bg=vibrant_colors['card'],
                              padx=25, pady=25, relief='raised', borderwidth=2)
    reflection_card.pack(fill='both', expand=True, pady=(0, 15))
    
    tk.Label(reflection_card, text="📝 Daily Reflection", 
             font=("Arial", 18, "bold"),
             bg=vibrant_colors['card'], fg=vibrant_colors['reflection']).pack(anchor='w', pady=(0, 15))
    
    # Reflection prompts
    reflection_prompts = """• How do you feel physically today?
• What was the highlight of your day?
• Any challenges with health/fitness?
• What are you grateful for today?
• Goals for tomorrow:"""
    
    app.reflection_text = scrolledtext.ScrolledText(reflection_card, 
                                                   font=("Arial", 12),
                                                   bg=colors['light_card'], fg='white',
                                                   wrap='word',
                                                   height=10,
                                                   padx=15, pady=15,
                                                   insertbackground='white')
    app.reflection_text.pack(fill='both', expand=True)
    
    # Insert existing data or prompts
    existing_reflection = today_data.get('reflection', '')
    if existing_reflection:
        app.reflection_text.insert("1.0", existing_reflection)
    else:
        app.reflection_text.insert("1.0", reflection_prompts)

    # ============ Bottom Save Area ============
    bottom_frame = tk.Frame(scrollable_frame, bg=colors['dark_bg'], height=120)
    bottom_frame.pack(fill='x', pady=(30, 20), padx=20)
    bottom_frame.pack_propagate(False)
    
    # Statistics (if records exist for today)
    if today_data:
        stats_frame = tk.Frame(bottom_frame, bg=colors['dark_bg'])
        stats_frame.pack(fill='x', pady=(0, 15))
        
        stats_text = f"📊 Today's Summary: Sleep {today_data.get('sleep', '--')}h • Water {today_data.get('water', '--')} cups • Mood {today_data.get('mood', '--')}/5"
        tk.Label(stats_frame, text=stats_text,
                font=("Arial", 12),
                bg=colors['dark_bg'], fg='#8b9bb4').pack()
    
    # Save button container
    save_container = tk.Frame(bottom_frame, bg=colors['dark_bg'])
    save_container.pack(expand=True)
    
    # Save button - large and prominent
    save_btn = tk.Button(save_container, text="💾 SAVE TODAY'S LOG", 
                        bg=vibrant_colors['save'], fg='white',
                        font=("Arial", 18, "bold"),
                        padx=50, pady=20,
                        relief='raised', borderwidth=3,
                        cursor="hand2",
                        command=lambda: save_daily_log(app))
    save_btn.pack()
    
    # Add hover effects
    def on_enter(e):
        save_btn.config(bg='#45a049', font=("Arial", 19, "bold"))
    
    def on_leave(e):
        save_btn.config(bg=vibrant_colors['save'], font=("Arial", 18, "bold"))
    
    save_btn.bind("<Enter>", on_enter)
    save_btn.bind("<Leave>", on_leave)
    
    # Bottom tip
    tip_label = tk.Label(bottom_frame, 
                        text="💡 Tip: Consistent logging helps identify patterns and improve health habits!",
                        font=("Arial", 10),
                        bg=colors['dark_bg'], fg='#8b9bb4')
    tip_label.pack(pady=(10, 0))
    
    # Bind mousewheel scrolling
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    canvas.bind_all("<MouseWheel>", on_mousewheel)
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
    
    # Set focus to first input field
    sleep_entry.focus_set()

def save_daily_log(app):
    """Save daily health log"""
    try:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Validate required inputs
        sleep_str = app.sleep_var.get().strip()
        water_str = app.water_var.get().strip()
        
        if not sleep_str or not water_str:
            messagebox.showerror("❌ Error", "Please fill in sleep hours and water intake!")
            return
        
        sleep = float(sleep_str)
        water = float(water_str)
        
        # Validate ranges
        if sleep < 0 or sleep > 24:
            messagebox.showerror("❌ Error", "Sleep hours must be between 0-24!")
            return
        
        if water < 0 or water > 50:
            messagebox.showerror("❌ Error", "Water intake seems unrealistic!")
            return
        
        # Get text content
        meals = app.meals_text.get("1.0", "end").strip()
        reflection = app.reflection_text.get("1.0", "end").strip()
        
        # Prepare data
        health_data = {
            "sleep": sleep,
            "water": water,
            "mood": app.mood_var.get(),
            "meals": meals,
            "reflection": reflection,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Use auth system to save data
        success = app.add_health_data(date, health_data)
        
        if success:
            # Show success message
            mood_emojis = ["😢", "😕", "😐", "😊", "😄"]
            mood_emoji = mood_emojis[app.mood_var.get() - 1] if 1 <= app.mood_var.get() <= 5 else "😐"
            
            success_msg = f"""✅ Successfully saved today's log!

📊 Summary:
• Sleep: {sleep} hours
• Water: {water} cups
• Mood: {mood_emoji} ({app.mood_var.get()}/5)
• Meals recorded: {len(meals.split('\\n')) if meals else 0} items
• Reflection: {'✓' if reflection else '✗'}

Keep up the great work! 💪"""
            
            messagebox.showinfo("✅ Log Saved", success_msg)
        else:
            messagebox.showerror("❌ Error", "Failed to save log!")
            
    except ValueError:
        messagebox.showerror("❌ Error", "Please enter valid numbers for sleep and water!")
    except Exception as e:
        messagebox.showerror("❌ Error", f"An error occurred: {str(e)}")

def load_today_data(app):
    """Load today's data"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    return app.health_data.get(today, {})