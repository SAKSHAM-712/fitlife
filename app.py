import os
from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key="AIzaSyDjiApNFuc3TbuLxZwD_cTb44iyJCwmhAQ")  # yaha apna valid Gemini API key lagana
# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

def make_prompt(user):
    return f"""
You are an expert Indian nutritionist + fitness coach.
User details:
Name: {user['name']}
Age: {user['age']}
Sex: {user['sex']}
Weight: {user['weight']} kg
Height: {user['height']} cm
Goal: {user['goal']}
Diet Preference: {user['diet']}
Activity Level: {user['activity']}
Fitness Level: {user['level']}

👉 Generate a structured HTML dashboard with the following sections:
1. **Calories & Macros** (show daily target calories, protein, carbs, fats)
2. **Meal Plan** (breakfast, lunch, dinner with dish, calories, servings)
3. **Workout Plan** (exercises, category, sets/reps, notes)
4. **Motivational Tip**

⚡IMPORTANT: 
- Reply ONLY in valid HTML (no JSON, no markdown).
- Use clean `<div>`, `<h2>`, `<ul>`, `<li>`, and `<table>` for formatting.
- Style it professionally (use inline CSS only for basic layout).
"""

# Home / Landing Page
@app.route("/")
def home():
    return render_template("index.html")

# Form Page for Personalized Plan
@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form.get("name", "User")
        age = int(request.form.get("age", 25))
        sex = request.form.get("sex", "male")
        weight = float(request.form.get("weight", 70))
        height = float(request.form.get("height", 170))
        activity = request.form.get("activity", "light")
        goal = request.form.get("goal", "maintain")
        diet = request.form.get("diet", "any")
        level = request.form.get("level", "beginner")

        user = {
            "name": name, "age": age, "sex": sex,
            "weight": weight, "height": height,
            "activity": activity, "goal": goal,
            "diet": diet, "level": level,
        }

        prompt = make_prompt(user)

        try:
            resp = model.generate_content(prompt)
            plan_html = resp.text if hasattr(resp, "text") else str(resp)
        except Exception as e:
            plan_html = f"<p style='color:red;'>ERROR_CALLING_GEMINI: {e}</p>"

        return render_template("result.html", user=user, plan=plan_html)

    return render_template("form.html")

# Meal Plan Page
@app.route("/meal")
def meal():
    meal_plan = [
        {"day": "Monday", "meals": ["Oats + Milk", "Grilled Chicken + Rice", "Salad + Soup"]},
        {"day": "Tuesday", "meals": ["Smoothie Bowl", "Paneer + Roti", "Fish + Veggies"]},
    ]
    return render_template("meal.html", meal_plan=meal_plan)

# Workouts Page
@app.route("/workouts")
def workouts():
    workouts = [
        {"day": "Monday", "routine": ["Push Ups", "Squats", "Plank"]},
        {"day": "Tuesday", "routine": ["Pull Ups", "Lunges", "Crunches"]},
    ]
    return render_template("workouts.html", workouts=workouts)

# Calories Page
@app.route("/calories")
def calories():
    calories = {
        "daily_goal": 2200,
        "consumed": 1850,
        "remaining": 350
    }
    return render_template("calories.html", calories=calories)

# Tips Page
@app.route("/tips")
def tips():
    tips = [
        "Drink at least 3 liters of water daily 💧",
        "Sleep 7-8 hours for muscle recovery 😴",
        "Avoid processed sugar ❌",
        "Do stretching before and after workouts 🧘"
    ]
    return render_template("tips.html", tips=tips)


if __name__ == "__main__":
    app.run(debug=True)
