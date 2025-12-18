import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import datetime

def on_mousewheel(event, canvas):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

def get_bmi_category_info(bmi):
    """Return classification information based on BMI value"""
    if bmi < 18.5:
        return {
            "category": "Underweight",
            "color": "#4FC3F7",
            "emoji": "💙",
            "message": "You may need to gain some weight",
            "advice": "• Increase calorie intake\n• Include protein-rich foods\n• Consider strength training"
        }
    elif bmi < 25:
        return {
            "category": "Normal",
            "color": "#81C784",
            "emoji": "✅",
            "message": "Great! You're at a healthy weight",
            "advice": "• Maintain balanced diet\n• Regular exercise\n• Stay hydrated"
        }
    elif bmi < 30:
        return {
            "category": "Overweight",
            "color": "#FFB74D",
            "emoji": "⚠️",
            "message": "Consider losing some weight",
            "advice": "• Reduce processed foods\n• Increase physical activity\n• Portion control"
        }
    else:
        return {
            "category": "Obese",
            "color": "#E57373",
            "emoji": "❗",
            "message": "Weight loss is recommended",
            "advice": "• Consult healthcare provider\n• Start gradual weight loss\n• Focus on whole foods"
        }

# ============ BMI Calculator Functions ============
def load_profile_data(app, height_entry, weight_entry):
    """Load BMI data from user profile"""
    try:
        user_profile = app.user_profile
        
        height = user_profile.get('height')
        weight = user_profile.get('weight')
        
        if height:
            app.height_var.set(str(height))
            if height_entry:
                height_entry.config(fg='#4CC9F0')  # Highlight display
            
        if weight:
            app.weight_var.set(str(weight))
            if weight_entry:
                weight_entry.config(fg='#4CC9F0')  # Highlight display
        
        messagebox.showinfo("✅ Profile Data Loaded", 
                           f"Height: {height if height else 'Not set'} cm\n"
                           f"Weight: {weight if weight else 'Not set'} kg")
        
        # Automatically calculate BMI
        if height and weight:
            calculate_bmi(app)
            
    except Exception as e:
        messagebox.showerror("❌ Error", f"Failed to load profile data: {str(e)}")

def update_profile_from_bmi(app):
    """Update user profile from BMI calculator"""
    try:
        height_str = app.height_var.get().strip()
        weight_str = app.weight_var.get().strip()
        
        if not height_str or not weight_str:
            messagebox.showerror("❌ Error", "Please enter height and weight first!")
            return
        
        height = float(height_str)
        weight = float(weight_str)
        
        if height < 50 or height > 250:
            messagebox.showerror("❌ Error", "Please enter a valid height (50-250 cm)!")
            return
        
        if weight < 20 or weight > 300:
            messagebox.showerror("❌ Error", "Please enter a valid weight (20-300 kg)!")
            return
        
        # Get existing profile
        user_profile = app.user_profile
        
        # Prepare update data
        profile_data = {
            "height": height,
            "weight": weight
        }
        
        # Preserve other fields
        if 'age' in user_profile:
            profile_data['age'] = user_profile['age']
        if 'gender' in user_profile:
            profile_data['gender'] = user_profile['gender']
        if 'email' in user_profile:
            profile_data['email'] = user_profile['email']
        if 'name' in user_profile:
            profile_data['name'] = user_profile['name']
        
        # Save updates
        success = app.save_profile(profile_data)
        
        if success:
            messagebox.showinfo("✅ Success", "Profile updated with new height and weight!")
        else:
            messagebox.showerror("❌ Error", "Failed to update profile!")
            
    except ValueError:
        messagebox.showerror("❌ Error", "Please enter valid numbers for height and weight!")
    except Exception as e:
        messagebox.showerror("❌ Error", f"An error occurred: {str(e)}")

def calculate_bmi(app):
    """Calculate BMI"""
    try:
        if not hasattr(app, 'height_var') or not hasattr(app, 'weight_var'):
            return
            
        height_str = app.height_var.get().strip()
        weight_str = app.weight_var.get().strip()
        
        if not height_str or not weight_str:
            messagebox.showerror("❌ Error", "Please enter both height and weight!")
            return
        
        height = float(height_str)
        weight = float(weight_str)
        
        if height <= 0 or weight <= 0:
            messagebox.showerror("❌ Error", "Values must be positive!")
            return
        
        if height < 50 or height > 250:
            messagebox.showerror("❌ Error", "Please enter a valid height (50-250 cm)!")
            return
            
        if weight < 20 or weight > 300:
            messagebox.showerror("❌ Error", "Please enter a valid weight (20-300 kg)!")
            return
            
        
        # Calculate BMI
        height_m = height / 100
        bmi = weight / (height_m * height_m)
        
        # Get classification information
        bmi_info = get_bmi_category_info(bmi)
        
        # Update emoji display
        if hasattr(app, 'bmi_emoji_label'):
            app.bmi_emoji_label.config(text=bmi_info["emoji"], fg=bmi_info["color"])
        
        # Update BMI value
        if hasattr(app, 'bmi_value_label'):
            app.bmi_value_label.config(text=f"BMI: {bmi:.1f}", fg=bmi_info["color"])
        
        # Update category
        if hasattr(app, 'bmi_category_label'):
            app.bmi_category_label.config(text=f"Category: {bmi_info['category']}", 
                                          fg=bmi_info["color"])
        
        # Update details
        if hasattr(app, 'bmi_details_text'):
            app.bmi_details_text.config(state='normal')
            app.bmi_details_text.delete("1.0", "end")
            
            # User information
            current_user = app.auth.get_current_user()
            user_profile = app.user_profile
            
            app.bmi_details_text.insert("end", f"📊 BMI Analysis for {current_user}\n")
            app.bmi_details_text.insert("end", f"{'═'*35}\n\n")
            
            app.bmi_details_text.insert("end", f"📏 Input Data:\n")
            app.bmi_details_text.insert("end", f"• Height: {height} cm\n")
            app.bmi_details_text.insert("end", f"• Weight: {weight} kg\n")
            app.bmi_details_text.insert("end", f"• BMI: {bmi:.1f}\n")
            app.bmi_details_text.insert("end", f"• Status: {bmi_info['message']}\n\n")
            
            # Calculate ideal weight range
            min_weight = 18.5 * (height_m * height_m)
            max_weight = 24.9 * (height_m * height_m)
            
            app.bmi_details_text.insert("end", f"🎯 Ideal Weight Range:\n")
            app.bmi_details_text.insert("end", f"• Minimum: {min_weight:.1f} kg\n")
            app.bmi_details_text.insert("end", f"• Maximum: {max_weight:.1f} kg\n")
            
            # Current status analysis
            if weight < min_weight:
                diff = min_weight - weight
                app.bmi_details_text.insert("end", f"• You are underweight by {diff:.1f} kg\n")
            elif weight > max_weight:
                diff = weight - max_weight
                app.bmi_details_text.insert("end", f"• You are overweight by {diff:.1f} kg\n")
            else:
                app.bmi_details_text.insert("end", f"• You are within the healthy range!\n")
            
            app.bmi_details_text.insert("end", f"\n💡 Health Advice:\n")
            app.bmi_details_text.insert("end", f"{'─'*15}\n")
            app.bmi_details_text.insert("end", f"{bmi_info['advice']}\n")
            
            # Add more suggestions based on age and gender from profile
            age = user_profile.get('age')
            gender = user_profile.get('gender', 'unknown')
            
            if age:
                app.bmi_details_text.insert("end", f"\n👤 Personalized for:\n")
                app.bmi_details_text.insert("end", f"• Age: {age} years\n")
                app.bmi_details_text.insert("end", f"• Gender: {gender.title()}\n")
            
            app.bmi_details_text.config(state='disabled')
        
    except ValueError:
        messagebox.showerror("❌ Error", "Please enter valid numbers for height and weight!")
    except Exception as e:
        messagebox.showerror("❌ Error", f"An error occurred: {str(e)}")

def save_bmi_record(app):
    """Save BMI record"""
    try:
        if hasattr(app, 'bmi_value_label'):
            bmi_text = app.bmi_value_label.cget("text")
            if bmi_text != "BMI: --":
                bmi_value = float(bmi_text.split(": ")[1])
                
                height_str = app.height_var.get().strip()
                weight_str = app.weight_var.get().strip()
                
                if height_str and weight_str:
                    height = float(height_str)
                    weight = float(weight_str)
                    
                    bmi_data = {
                        "bmi": bmi_value,
                        "height": height,
                        "weight": weight,
                        "date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    # Save to auth system
                    success = app.add_bmi_record(bmi_data)
                    
                    if success:
                        messagebox.showinfo("✅ Success", "BMI record saved successfully!\n\n" +
                                          f"{bmi_text}\n" +
                                          f"Height: {height} cm\n" +
                                          f"Weight: {weight} kg\n" +
                                          f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}")
                    else:
                        messagebox.showerror("❌ Error", "Failed to save BMI record!")
                else:
                    messagebox.showwarning("⚠️ Warning", "Height and weight data not available!")
            else:
                messagebox.showwarning("⚠️ Warning", "Please calculate BMI first!")
    except Exception as e:
        messagebox.showerror("❌ Error", f"Failed to save record: {str(e)}")

# ============ Calorie Calculator Functions ============
def calculate_calories_func(app):
    """Calculate daily calorie needs"""
    try:
        if not hasattr(app, 'age_var') or not hasattr(app, 'gender_var') or not hasattr(app, 'activity_var') or not hasattr(app, 'goal_var'):
            return
            
        # Get all necessary inputs
        age_str = app.age_var.get().strip()
        if not age_str:
            messagebox.showerror("❌ Error", "Please enter your age!")
            return
        
        age = int(age_str)
        gender = app.gender_var.get()
        activity = app.activity_var.get()
        goal = app.goal_var.get()
        
        # Need height and weight data from BMI page
        height_str = app.height_var.get().strip()
        weight_str = app.weight_var.get().strip()
        
        height = None
        weight = None
        
        if height_str:
            height = float(height_str)
        if weight_str:
            weight = float(weight_str)
        
        # If height/weight not set, use defaults
        if not height or not weight:
            messagebox.showwarning("⚠️", "Using default values for height/weight")
            height = height if height else 170
            weight = weight if weight else 65
        
        # Calculate BMR (Basal Metabolic Rate)
        if gender == "male":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        
        # Activity level multipliers
        activity_multipliers = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "very_active": 1.9
        }
        
        tdee = bmr * activity_multipliers.get(activity, 1.55)
        
        # Adjust calories based on goal
        if goal == "lose":
            target_calories = tdee - 500
        elif goal == "gain":
            target_calories = tdee + 500
        else:
            target_calories = tdee
        
        # Update calorie value display
        if hasattr(app, 'calorie_value_label'):
            app.calorie_value_label.config(text=f"{target_calories:.0f} calories/day")
        
        # Update details
        if hasattr(app, 'calorie_details_text'):
            app.calorie_details_text.config(state='normal')
            app.calorie_details_text.delete("1.0", "end")
            
            app.calorie_details_text.insert("end", f"🔥 Your Daily Calorie Needs\n")
            app.calorie_details_text.insert("end", f"{'═'*35}\n\n")
            
            app.calorie_details_text.insert("end", f"📊 Personal Information:\n")
            app.calorie_details_text.insert("end", f"• Age: {age} years\n")
            app.calorie_details_text.insert("end", f"• Gender: {gender.title()}\n")
            app.calorie_details_text.insert("end", f"• Height: {height} cm\n")
            app.calorie_details_text.insert("end", f"• Weight: {weight} kg\n")
            app.calorie_details_text.insert("end", f"• Activity Level: {activity.replace('_', ' ').title()}\n")
            app.calorie_details_text.insert("end", f"• Goal: {goal.replace('_', ' ').title()}\n\n")
            
            app.calorie_details_text.insert("end", f"📈 Calculations:\n")
            app.calorie_details_text.insert("end", f"• BMR (Basal Metabolic Rate): {bmr:.0f} calories/day\n")
            app.calorie_details_text.insert("end", f"• TDEE (Total Daily Energy Expenditure): {tdee:.0f} calories/day\n\n")
            
            app.calorie_details_text.insert("end", f"🎯 Recommended Daily Intake:\n")
            app.calorie_details_text.insert("end", f"• Target Calories: {target_calories:.0f} calories/day\n\n")
            
            # Add advice
            app.calorie_details_text.insert("end", f"💡 Tips for your goal:\n")
            if goal == "lose":
                app.calorie_details_text.insert("end", f"• Create a 500-calorie deficit daily\n")
                app.calorie_details_text.insert("end", f"• Aim for 0.5-1kg weight loss per week\n")
                app.calorie_details_text.insert("end", f"• Combine diet with exercise\n")
            elif goal == "gain":
                app.calorie_details_text.insert("end", f"• Create a 500-calorie surplus daily\n")
                app.calorie_details_text.insert("end", f"• Focus on protein-rich foods\n")
                app.calorie_details_text.insert("end", f"• Include strength training\n")
            else:
                app.calorie_details_text.insert("end", f"• Maintain current calorie intake\n")
                app.calorie_details_text.insert("end", f"• Focus on nutrient balance\n")
                app.calorie_details_text.insert("end", f"• Regular exercise for health\n")
            
            app.calorie_details_text.config(state='disabled')
        
    except ValueError:
        messagebox.showerror("❌ Error", "Please enter valid numbers!")
    except Exception as e:
        messagebox.showerror("❌ Error", f"An error occurred: {str(e)}")

# ============ Helper Functions ============
def select_gender(value, gender_buttons, vibrant_colors, app):
    app.gender_var.set(value)
    update_gender_display(gender_buttons, vibrant_colors, app)

def update_gender_display(gender_buttons, vibrant_colors, app):
    selected_value = app.gender_var.get()
    
    for btn in gender_buttons:
        if btn["value"] == selected_value:
            # Selected state
            btn["frame"].config(bg=btn["color"], relief='sunken')
            btn["emoji"].config(bg=btn["color"], font=("Arial", 32, "bold"))
            btn["text"].config(bg=btn["color"], font=("Arial", 12, "bold"), fg='white')
            btn["indicator"].config(bg=btn["color"], fg='white')
            btn["selected"] = True
        else:
            # Unselected state
            btn["frame"].config(bg=vibrant_colors['card'], relief='flat')
            btn["emoji"].config(bg=vibrant_colors['card'], font=("Arial", 28))
            btn["text"].config(bg=vibrant_colors['card'], font=("Arial", 12), fg='white')
            btn["indicator"].config(bg=vibrant_colors['card'], fg=vibrant_colors['card'])
            btn["selected"] = False

def select_activity(value, activity_buttons, vibrant_colors, app):
    app.activity_var.set(value)
    update_activity_display(activity_buttons, vibrant_colors, app)

def update_activity_display(activity_buttons, vibrant_colors, app):
    selected_value = app.activity_var.get()
    
    for btn in activity_buttons:
        if btn["value"] == selected_value:
            # Selected state
            btn["frame"].config(bg=btn["color"], relief='sunken')
            btn["emoji"].config(bg=btn["color"])
            btn["text"].config(bg=btn["color"], fg='white')
            btn["indicator"].config(bg=btn["color"], fg='white')
            btn["selected"] = True
        else:
            # Unselected state
            btn["frame"].config(bg=vibrant_colors['card'], relief='flat')
            btn["emoji"].config(bg=vibrant_colors['card'])
            btn["text"].config(bg=vibrant_colors['card'], fg='white')
            btn["indicator"].config(bg=vibrant_colors['card'], fg=vibrant_colors['card'])
            btn["selected"] = False

def select_goal(value, goal_buttons, vibrant_colors, app):
    app.goal_var.set(value)
    update_goal_display(goal_buttons, vibrant_colors, app)

def update_goal_display(goal_buttons, vibrant_colors, app):
    selected_value = app.goal_var.get()
    
    for btn in goal_buttons:
        if btn["value"] == selected_value:
            # Selected state
            btn["frame"].config(bg=btn["color"], relief='sunken')
            btn["emoji"].config(bg=btn["color"])
            btn["text"].config(bg=btn["color"], fg='white')
            btn["indicator"].config(bg=btn["color"], fg='white')
            btn["selected"] = True
        else:
            # Unselected state
            btn["frame"].config(bg=vibrant_colors['card'], relief='flat')
            btn["emoji"].config(bg=vibrant_colors['card'])
            btn["text"].config(bg=vibrant_colors['card'], fg='white')
            btn["indicator"].config(bg=vibrant_colors['card'], fg=vibrant_colors['card'])
            btn["selected"] = False

# ============ Main Function ============
def bmi_calorie_calculator(app):
    """Main function for BMI and Calorie Calculator"""
    if not app.auth.is_logged_in():
        app.show_login_screen()
        return
    
    app.clear_frame()
    colors = app.colors
    root = app.root
    
    # Set larger emoji font
    large_emoji_font = ("Arial", 40, "bold")
    
    # Define vibrant color scheme
    vibrant_colors = {
        'bmi': '#FF6B6B',      # Red - BMI calculation
        'calorie': '#4ECDC4',   # Cyan - Calorie calculation
        'ideal': '#45B7D1',     # Blue - Ideal weight
        'history': '#96CEB4',   # Green - History records
        'card': '#1A1F2C',      # Card background
        'save': '#4CAF50',      # Green - Save button
        'input': '#2A3648'      # Input field background
    }
    
    # Get user profile data
    user_profile = app.user_profile
    
    # Main frame
    main_frame = tk.Frame(root, bg=colors['dark_bg'])
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Top navigation bar
    top_frame = tk.Frame(main_frame, bg=colors['dark_bg'])
    top_frame.pack(fill='x', pady=(0, 20))
    
    # Back button
    back_btn = tk.Button(top_frame, text="← Back to Main Menu", 
                        command=app.show_main_menu,
                        bg=colors['secondary'], fg='white',
                        font=("Arial", 12, "bold"),
                        padx=20, pady=8)
    back_btn.pack(side='left')
    
    # Title
    title_label = tk.Label(top_frame, text="⚖️ BMI & Calorie Calculator",
                          font=("Arial", 28, "bold"),
                          bg=colors['dark_bg'], fg='white')
    title_label.pack(side='left', padx=50)
    
    # Create Notebook (tab container)
    notebook = ttk.Notebook(main_frame)
    notebook.pack(fill='both', expand=True)
    
    # Custom tab style
    style = ttk.Style()
    style.configure('TNotebook.Tab', font=('Arial', 12, 'bold'), padding=[15, 8])
    style.map('TNotebook.Tab', background=[('selected', vibrant_colors['bmi'])])
    
    # ============ Tab 1: BMI Calculator ============
    tab1_frame = tk.Frame(notebook, bg=colors['dark_bg'])
    notebook.add(tab1_frame, text="🧮 BMI Calculator")
    
    # Content area (using Canvas for scrolling)
    tab1_canvas = tk.Canvas(tab1_frame, bg=colors['dark_bg'], highlightthickness=0)
    tab1_scrollbar = tk.Scrollbar(tab1_frame, orient="vertical", command=tab1_canvas.yview)
    tab1_scrollable = tk.Frame(tab1_canvas, bg=colors['dark_bg'])
    
    tab1_scrollable.bind(
        "<Configure>",
        lambda e: tab1_canvas.configure(scrollregion=tab1_canvas.bbox("all"))
    )
    
    tab1_canvas.create_window((0, 0), window=tab1_scrollable, anchor="nw")
    tab1_canvas.configure(yscrollcommand=tab1_scrollbar.set)
    
    tab1_canvas.pack(side="left", fill="both", expand=True)
    tab1_scrollbar.pack(side="right", fill="y")
    
    # Calculator content
    tab1_content = tk.Frame(tab1_scrollable, bg=colors['dark_bg'])
    tab1_content.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Left-right split
    tab1_left = tk.Frame(tab1_content, bg=colors['dark_bg'])
    tab1_left.pack(side='left', fill='both', expand=True, padx=10)
    
    tab1_right = tk.Frame(tab1_content, bg=colors['dark_bg'])
    tab1_right.pack(side='right', fill='both', expand=True, padx=10)
    
    # === Left column: Input ===
    input_card = tk.Frame(tab1_left, bg=vibrant_colors['card'], 
                         padx=25, pady=25, relief='raised', borderwidth=2)
    input_card.pack(fill='both', expand=True)
    
    tk.Label(input_card, text="📏 Personal Information",
             font=("Arial", 20, "bold"),
             bg=vibrant_colors['card'], fg=vibrant_colors['bmi']).pack(anchor='w', pady=(0, 20))
    
    # Height input
    height_frame = tk.Frame(input_card, bg=vibrant_colors['card'])
    height_frame.pack(fill='x', pady=(0, 15))
    
    tk.Label(height_frame, text="📏 Height (cm)", 
             font=("Arial", 14, "bold"),
             bg=vibrant_colors['card'], fg='white').pack(anchor='w')
    
    app.height_var = tk.StringVar(value=str(user_profile.get('height', '')))
    height_entry = tk.Entry(height_frame, textvariable=app.height_var,
                           font=("Arial", 16),
                           bg=vibrant_colors['input'], fg='white',
                           insertbackground='white',
                           relief='flat', borderwidth=2)
    height_entry.pack(fill='x', pady=(8, 0), ipady=8)
    
    # Weight input
    weight_frame = tk.Frame(input_card, bg=vibrant_colors['card'])
    weight_frame.pack(fill='x', pady=(0, 25))
    
    tk.Label(weight_frame, text="⚖️ Weight (kg)", 
             font=("Arial", 14, "bold"),
             bg=vibrant_colors['card'], fg='white').pack(anchor='w')
    
    app.weight_var = tk.StringVar(value=str(user_profile.get('weight', '')))
    weight_entry = tk.Entry(weight_frame, textvariable=app.weight_var,
                           font=("Arial", 16),
                           bg=vibrant_colors['input'], fg='white',
                           insertbackground='white',
                           relief='flat', borderwidth=2)
    weight_entry.pack(fill='x', pady=(8, 0), ipady=8)
    
    # Buttons to apply user profile data
    profile_actions_frame = tk.Frame(input_card, bg=vibrant_colors['card'])
    profile_actions_frame.pack(fill='x', pady=(0, 20))
    
    # Display current profile info
    if user_profile.get('height') and user_profile.get('weight'):
        profile_info = f"Your Profile: {user_profile.get('height', '--')}cm, {user_profile.get('weight', '--')}kg"
        tk.Label(profile_actions_frame, text=profile_info,
                font=("Arial", 10),
                bg=vibrant_colors['card'], fg='#8b9bb4').pack(pady=(0, 10))
    
    # Apply profile data button
    use_profile_btn = tk.Button(profile_actions_frame, text="🔄 Use My Profile Data",
                               bg='#45B7D1', fg='white',
                               font=("Arial", 12, "bold"),
                               padx=20, pady=10,
                               command=lambda: load_profile_data(app, height_entry, weight_entry))
    use_profile_btn.pack(side='left', padx=(0, 10))
    
    # Update profile button
    update_profile_btn = tk.Button(profile_actions_frame, text="💾 Update Profile",
                                  bg='#4CAF50', fg='white',
                                  font=("Arial", 12),
                                  padx=20, pady=10,
                                  command=lambda: update_profile_from_bmi(app))
    update_profile_btn.pack(side='left')
    
    # Calculate button
    calc_btn = tk.Button(input_card, text="🔢 Calculate BMI",
                        bg=vibrant_colors['bmi'], fg='white',
                        font=("Arial", 16, "bold"),
                        padx=30, pady=15,
                        command=lambda: calculate_bmi(app))
    calc_btn.pack()
    
    # === Right column: Results ===
    results_card = tk.Frame(tab1_right, bg=vibrant_colors['card'], 
                           padx=25, pady=25, relief='raised', borderwidth=2)
    results_card.pack(fill='both', expand=True)
    
    tk.Label(results_card, text="📊 Results",
             font=("Arial", 20, "bold"),
             bg=vibrant_colors['card'], fg=vibrant_colors['bmi']).pack(anchor='w', pady=(0, 20))
    
    # Large emoji display area
    app.bmi_emoji_label = tk.Label(results_card, text="📈",
                                  font=large_emoji_font,
                                  bg=vibrant_colors['card'])
    app.bmi_emoji_label.pack(pady=(10, 20))
    
    # BMI value display
    app.bmi_value_label = tk.Label(results_card, text="BMI: --",
                                  font=("Arial", 36, "bold"),
                                  bg=vibrant_colors['card'], fg='white')
    app.bmi_value_label.pack(pady=(0, 10))
    
    # Category display
    app.bmi_category_label = tk.Label(results_card, text="Category: --",
                                      font=("Arial", 20),
                                      bg=vibrant_colors['card'], fg='white')
    app.bmi_category_label.pack(pady=(0, 20))
    
    # Details text box
    app.bmi_details_text = scrolledtext.ScrolledText(results_card,
                                                    bg=vibrant_colors['input'],
                                                    fg='white',
                                                    font=("Arial", 11),
                                                    wrap='word',
                                                    height=8,
                                                    padx=15, pady=15)
    app.bmi_details_text.pack(fill='both', expand=True, pady=(10, 0))
    
    # Save button
    save_bmi_btn = tk.Button(results_card, text="💾 Save BMI Record",
                            bg=vibrant_colors['save'], fg='white',
                            font=("Arial", 14, "bold"),
                            padx=30, pady=12,
                            command=lambda: save_bmi_record(app))
    save_bmi_btn.pack(pady=(20, 0))
    
    # ============ Tab 2: Calorie Calculator ============
    tab2_frame = tk.Frame(notebook, bg=colors['dark_bg'])
    notebook.add(tab2_frame, text="🔥 Calorie Calculator")
    
    # Content area (using Canvas for scrolling) - increase height
    tab2_canvas = tk.Canvas(tab2_frame, bg=colors['dark_bg'], highlightthickness=0, height=700)
    tab2_scrollbar = tk.Scrollbar(tab2_frame, orient="vertical", command=tab2_canvas.yview)
    tab2_scrollable = tk.Frame(tab2_canvas, bg=colors['dark_bg'])
    
    tab2_scrollable.bind(
        "<Configure>",
        lambda e: tab2_canvas.configure(scrollregion=tab2_canvas.bbox("all"))
    )
    
    tab2_canvas.create_window((0, 0), window=tab2_scrollable, anchor="nw")
    tab2_canvas.configure(yscrollcommand=tab2_scrollbar.set)
    
    tab2_canvas.pack(side="left", fill="both", expand=True)
    tab2_scrollbar.pack(side="right", fill="y")
    
    # Calorie calculator content - increase padding
    tab2_content = tk.Frame(tab2_scrollable, bg=colors['dark_bg'])
    tab2_content.pack(fill='both', expand=True, padx=20, pady=10)
    
    # Create main container for calorie calculator
    calorie_main_frame = tk.Frame(tab2_content, bg=colors['dark_bg'])
    calorie_main_frame.pack(fill='both', expand=True)
    
    # Calorie calculator title
    calorie_title_frame = tk.Frame(calorie_main_frame, bg=colors['dark_bg'])
    calorie_title_frame.pack(fill='x', pady=(0, 20))
    
    tk.Label(calorie_title_frame, text="🔥 Calorie Calculator",
             font=("Arial", 24, "bold"),
             bg=colors['dark_bg'], fg='white').pack()
    
    # Left-right split - maintain consistent layout with BMI calculator
    tab2_left = tk.Frame(calorie_main_frame, bg=colors['dark_bg'])
    tab2_left.pack(side='left', fill='both', expand=True, padx=10)
    
    tab2_right = tk.Frame(calorie_main_frame, bg=colors['dark_bg'])
    tab2_right.pack(side='right', fill='both', expand=True, padx=10)
    
    # === Left column: Input ===
    calorie_input_card = tk.Frame(tab2_left, bg=vibrant_colors['card'], 
                                 padx=25, pady=25, relief='raised', borderwidth=2)
    calorie_input_card.pack(fill='both', expand=True)
    
    # Input area title
    input_title_frame = tk.Frame(calorie_input_card, bg=vibrant_colors['card'])
    input_title_frame.pack(fill='x', pady=(0, 20))
    
    tk.Label(input_title_frame, text="📝 Input Parameters",
             font=("Arial", 20, "bold"),
             bg=vibrant_colors['card'], fg=vibrant_colors['calorie']).pack(anchor='w')
    
    # Age
    age_frame = tk.Frame(calorie_input_card, bg=vibrant_colors['card'])
    age_frame.pack(fill='x', pady=(0, 20))
    
    tk.Label(age_frame, text="🎂 Age", 
             font=("Arial", 14, "bold"),
             bg=vibrant_colors['card'], fg='white').pack(anchor='w', pady=(0, 8))
    
    app.age_var = tk.StringVar(value=str(user_profile.get('age', '')))
    age_entry = tk.Entry(age_frame, textvariable=app.age_var,
                         font=("Arial", 16),
                         bg=vibrant_colors['input'], fg='white',
                         width=20)
    age_entry.pack(fill='x', pady=(0, 0), ipady=8)
    
    # Gender selection
    gender_frame = tk.Frame(calorie_input_card, bg=vibrant_colors['card'])
    gender_frame.pack(fill='x', pady=(0, 20))
    
    tk.Label(gender_frame, text="👥 Gender", 
             font=("Arial", 14, "bold"),
             bg=vibrant_colors['card'], fg='white').pack(anchor='w', pady=(0, 8))
    
    # Gender selection buttons - use horizontal layout
    gender_btn_frame = tk.Frame(gender_frame, bg=vibrant_colors['card'])
    gender_btn_frame.pack(fill='x', pady=(5, 0))
    
    app.gender_var = tk.StringVar(value=user_profile.get('gender', 'male'))
    gender_buttons = []
    
    # Create custom gender selection buttons
    gender_options = [
        {"emoji": "👨", "text": "Male", "value": "male", "color": "#4FC3F7"},
        {"emoji": "👩", "text": "Female", "value": "female", "color": "#F06292"}
    ]
    
    for i, option in enumerate(gender_options):
        btn_container = tk.Frame(gender_btn_frame, bg=vibrant_colors['card'])
        btn_container.pack(side='left', padx=(0, 15) if i == 0 else (0, 0))
        
        # Create clickable frame
        clickable_frame = tk.Frame(btn_container, bg=vibrant_colors['card'], 
                                  relief='flat', borderwidth=2, cursor="hand2")
        clickable_frame.pack()
        
        # Large emoji label
        emoji_label = tk.Label(clickable_frame, 
                              text=option["emoji"],
                              font=("Arial", 28, "bold"),
                              bg=vibrant_colors['card'],
                              fg='white')
        emoji_label.pack()
        
        # Text label
        text_label = tk.Label(clickable_frame, 
                             text=option["text"],
                             font=("Arial", 12),
                             bg=vibrant_colors['card'],
                             fg='white')
        text_label.pack(pady=(5, 8))
        
        # Circular selection indicator
        indicator = tk.Label(clickable_frame, 
                            text="●",
                            font=("Arial", 16),
                            bg=vibrant_colors['card'],
                            fg=vibrant_colors['card'])  # Initially transparent
        indicator.pack()
        
        # Store button info
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
            widget.bind("<Button-1>", lambda e, v=option["value"]: select_gender(v, gender_buttons, vibrant_colors, app))
    
    # Activity level selection
    activity_frame = tk.Frame(calorie_input_card, bg=vibrant_colors['card'])
    activity_frame.pack(fill='x', pady=(0, 20))
    
    tk.Label(activity_frame, text="🏃 Activity Level", 
             font=("Arial", 14, "bold"),
             bg=vibrant_colors['card'], fg='white').pack(anchor='w', pady=(0, 8))
    
    app.activity_var = tk.StringVar(value="moderate")
    activity_buttons = []
    
    activity_options = [
        {"emoji": "🛋️", "text": "Sedentary", "value": "sedentary", "color": "#90A4AE"},
        {"emoji": "🚶", "text": "Light", "value": "light", "color": "#81C784"},
        {"emoji": "💪", "text": "Moderate", "value": "moderate", "color": "#4DD0E1"},
        {"emoji": "🏋️", "text": "Active", "value": "active", "color": "#FFB74D"},
        {"emoji": "🔥", "text": "Very Active", "value": "very_active", "color": "#E57373"}
    ]
    
    # Create horizontal layout container
    activity_container = tk.Frame(activity_frame, bg=vibrant_colors['card'])
    activity_container.pack(fill='x', pady=(5, 0))
    
    # Create frame for activity level options
    activity_options_frame = tk.Frame(activity_container, bg=vibrant_colors['card'])
    activity_options_frame.pack(fill='x')
    
    # Create two-row layout
    row1_frame = tk.Frame(activity_options_frame, bg=vibrant_colors['card'])
    row1_frame.pack(fill='x', pady=(0, 5))
    
    row2_frame = tk.Frame(activity_options_frame, bg=vibrant_colors['card'])
    row2_frame.pack(fill='x')
    
    for i, option in enumerate(activity_options):
        # Decide which row to place in
        if i < 3:
            row = row1_frame
        else:
            row = row2_frame
            
        btn_container = tk.Frame(row, bg=vibrant_colors['card'])
        btn_container.pack(side='left', padx=(0, 10) if i < len(activity_options)-1 else (0, 0), pady=5, expand=True, fill='x')
        
        # Create clickable frame
        clickable_frame = tk.Frame(btn_container, bg=vibrant_colors['card'], 
                                  relief='flat', borderwidth=2, cursor="hand2")
        clickable_frame.pack(fill='both', expand=True)
        
        # Emoji label
        emoji_label = tk.Label(clickable_frame, 
                              text=option["emoji"],
                              font=("Arial", 20, "bold"),
                              bg=vibrant_colors['card'],
                              fg='white')
        emoji_label.pack(pady=(10, 0))
        
        # Text label
        text_label = tk.Label(clickable_frame, 
                             text=option["text"],
                             font=("Arial", 11, "bold"),
                             bg=vibrant_colors['card'],
                             fg='white')
        text_label.pack()
        
        # Circular selection indicator
        indicator = tk.Label(clickable_frame, 
                            text="●",
                            font=("Arial", 12),
                            bg=vibrant_colors['card'],
                            fg=vibrant_colors['card'])  # Initially transparent
        indicator.pack(pady=(0, 5))
        
        # Store button info
        activity_buttons.append({
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
            widget.bind("<Button-1>", lambda e, v=option["value"]: select_activity(v, activity_buttons, vibrant_colors, app))
    
    # Goal selection
    goal_frame = tk.Frame(calorie_input_card, bg=vibrant_colors['card'])
    goal_frame.pack(fill='x', pady=(0, 20))
    
    tk.Label(goal_frame, text="🎯 Goal", 
             font=("Arial", 14, "bold"),
             bg=vibrant_colors['card'], fg='white').pack(anchor='w', pady=(0, 8))
    
    app.goal_var = tk.StringVar(value="maintain")
    goal_buttons = []
    
    goal_options = [
        {"emoji": "⬇️", "text": "Lose Weight", "value": "lose", "color": "#4FC3F7"},
        {"emoji": "⚖️", "text": "Maintain", "value": "maintain", "color": "#81C784"},
        {"emoji": "⬆️", "text": "Gain Weight", "value": "gain", "color": "#FFB74D"}
    ]
    
    # Create horizontal layout
    goal_btn_frame = tk.Frame(goal_frame, bg=vibrant_colors['card'])
    goal_btn_frame.pack(fill='x', pady=(5, 0))
    
    for i, option in enumerate(goal_options):
        btn_container = tk.Frame(goal_btn_frame, bg=vibrant_colors['card'])
        btn_container.pack(side='left', padx=(0, 15) if i < len(goal_options)-1 else (0, 0), expand=True, fill='x')
        
        # Create clickable frame
        clickable_frame = tk.Frame(btn_container, bg=vibrant_colors['card'], 
                                  relief='flat', borderwidth=2, cursor="hand2")
        clickable_frame.pack(fill='both', expand=True)
        
        # Emoji label
        emoji_label = tk.Label(clickable_frame, 
                              text=option["emoji"],
                              font=("Arial", 20, "bold"),
                              bg=vibrant_colors['card'],
                              fg='white')
        emoji_label.pack(pady=(10, 0))
        
        # Text label
        text_label = tk.Label(clickable_frame, 
                             text=option["text"],
                             font=("Arial", 11, "bold"),
                             bg=vibrant_colors['card'],
                             fg='white')
        text_label.pack()
        
        # Circular selection indicator
        indicator = tk.Label(clickable_frame, 
                            text="●",
                            font=("Arial", 12),
                            bg=vibrant_colors['card'],
                            fg=vibrant_colors['card'])  # Initially transparent
        indicator.pack(pady=(0, 5))
        
        # Store button info
        goal_buttons.append({
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
            widget.bind("<Button-1>", lambda e, v=option["value"]: select_goal(v, goal_buttons, vibrant_colors, app))
    
    # Use profile data button
    profile_frame = tk.Frame(calorie_input_card, bg=vibrant_colors['card'])
    profile_frame.pack(fill='x', pady=(10, 20))
    
    # Define new load_profile_calorie_data function inside calorie calculator
    def load_profile_calorie_data_local():
        """Load calorie calculation data from user profile (local version)"""
        try:
            user_profile = app.user_profile
            
            age = user_profile.get('age')
            gender = user_profile.get('gender', 'male')
            
            if age:
                app.age_var.set(str(age))
                if age_entry:
                    age_entry.config(fg='#4CC9F0')  # Highlight display
            
            if gender:
                app.gender_var.set(gender)
            
            # Update display
            update_gender_display(gender_buttons, vibrant_colors, app)
            update_activity_display(activity_buttons, vibrant_colors, app)
            update_goal_display(goal_buttons, vibrant_colors, app)
            
            if age or gender:
                messagebox.showinfo("✅ Profile Data Loaded", 
                                   f"Age: {age if age else 'Not set'}\n"
                                   f"Gender: {gender.title()}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to load profile data: {str(e)}")
    
    use_profile_calorie_btn = tk.Button(profile_frame, text="🔄 Use Profile Data",
                                       bg='#45B7D1', fg='white',
                                       font=("Arial", 12, "bold"),
                                       padx=20, pady=10,
                                       command=load_profile_calorie_data_local)  # Use local function
    use_profile_calorie_btn.pack()
    
    # Calculate calories button - ensure visible within card
    calc_button_frame = tk.Frame(calorie_input_card, bg=vibrant_colors['card'])
    calc_button_frame.pack(fill='x', pady=(10, 0))
    
    calc_calorie_btn = tk.Button(calc_button_frame, text="🔥 Calculate Calories",
                                bg=vibrant_colors['calorie'], fg='white',
                                font=("Arial", 16, "bold"),
                                padx=30, pady=15,
                                command=lambda: calculate_calories_func(app))
    calc_calorie_btn.pack()
    
    # === Right column: Results ===
    calorie_results_card = tk.Frame(tab2_right, bg=vibrant_colors['card'], 
                                   padx=25, pady=25, relief='raised', borderwidth=2)
    calorie_results_card.pack(fill='both', expand=True)
    
    tk.Label(calorie_results_card, text="📊 Calorie Results",
             font=("Arial", 20, "bold"),
             bg=vibrant_colors['card'], fg=vibrant_colors['calorie']).pack(anchor='w', pady=(0, 20))
    
    # Large emoji display area
    calorie_emoji_label = tk.Label(calorie_results_card, text="🔥",
                                  font=large_emoji_font,
                                  bg=vibrant_colors['card'], fg=vibrant_colors['calorie'])
    calorie_emoji_label.pack(pady=(10, 20))
    
    # Calorie result title
    calorie_title_label = tk.Label(calorie_results_card, text="Daily Calorie Needs",
                                  font=("Arial", 24, "bold"),
                                  bg=vibrant_colors['card'], fg='white')
    calorie_title_label.pack(pady=(0, 10))
    
    # Calorie value display
    app.calorie_value_label = tk.Label(calorie_results_card, text="-- calories/day",
                                      font=("Arial", 36, "bold"),
                                      bg=vibrant_colors['card'], fg=vibrant_colors['calorie'])
    app.calorie_value_label.pack(pady=(0, 20))
    
    # Details text box
    app.calorie_details_text = scrolledtext.ScrolledText(calorie_results_card,
                                                        bg=vibrant_colors['input'],
                                                        fg='white',
                                                        font=("Arial", 11),
                                                        wrap='word',
                                                        height=8,
                                                        padx=15, pady=15)
    app.calorie_details_text.pack(fill='both', expand=True, pady=(10, 0))
    
    # Add hover effects for gender, activity level, goal buttons
    def add_hover_effects(buttons):
        for btn in buttons:
            for widget in [btn["frame"], btn["emoji"], btn["text"], btn["indicator"]]:
                widget.bind("<Enter>", lambda e, b=btn: on_button_hover(e, b))
                widget.bind("<Leave>", lambda e, b=btn: on_button_leave(e, b, vibrant_colors))
    
    def on_button_hover(event, button_info):
        if not button_info["selected"]:
            button_info["frame"].config(bg=button_info["color"])
            button_info["emoji"].config(bg=button_info["color"])
            button_info["text"].config(bg=button_info["color"])
            button_info["indicator"].config(bg=button_info["color"])
    
    def on_button_leave(event, button_info, vibrant_colors):
        if not button_info["selected"]:
            button_info["frame"].config(bg=vibrant_colors['card'])
            button_info["emoji"].config(bg=vibrant_colors['card'])
            button_info["text"].config(bg=vibrant_colors['card'])
            button_info["indicator"].config(bg=vibrant_colors['card'])
    
    # Apply hover effects
    add_hover_effects(gender_buttons)
    add_hover_effects(activity_buttons)
    add_hover_effects(goal_buttons)
    
    # Initialize display
    update_gender_display(gender_buttons, vibrant_colors, app)
    update_activity_display(activity_buttons, vibrant_colors, app)
    update_goal_display(goal_buttons, vibrant_colors, app)
    
    # Bind mousewheel events
    def bind_mousewheel(canvas):
        canvas.bind_all("<MouseWheel>", lambda e: on_mousewheel(e, canvas))
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
    
    bind_mousewheel(tab1_canvas)
    bind_mousewheel(tab2_canvas)
    
    # Automatically load user profile data
    load_profile_data(app, height_entry, weight_entry)
    load_profile_calorie_data_local()  # Use local function