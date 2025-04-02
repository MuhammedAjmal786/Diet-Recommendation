# Libraries
from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import re
import string

# Initialize the Flask app
app = Flask(__name__)

# Load Dataset
df = pd.read_csv('food.csv')

# Creating function for clean column Name
def preprocess_text(text):
    text = re.sub(r'[@#$%^&*!`~-]', '', text)  # Removes special characters
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = text.strip()  # Remove leading and trailing whitespaces
    return text
df['Name'] = df['Name'].apply(preprocess_text)

# Creating function for clean column RecipeInstructions
def clean_instructions(text):
        text = text.lstrip('c("').rstrip('",)') # Remove the 'c' at the start and quotes
        text = text.translate(str.maketrans("", "", string.punctuation))# Remove any remaining special characters if needed
        return text

    # Appling function
df['RecipeInstructions'] = df['RecipeInstructions'].apply(clean_instructions)

    # Calculations functions

    # Calculate BMR using Mifflin-St Jeor Formula
def calculate_bmr(weight, height, age, sex):
        if sex == "male":
            return (9.99 * weight) + (6.25 * height) - (4.92 * age) + 5
        else: # female
            return (9.99 * weight) + (6.25 * height) - (4.92 * age) - 161

    # Calculate Total Daily Energy Expenditure based on activity levels
def calculate_tdee(bmr, activity_level):
        activity_lvls = {
            "sedentary": 1.2,
            "lightly_active": 1.375,
            "moderate": 1.55,
            "very_active": 1.725,
            "extra_active": 1.9
        }
        return bmr * activity_lvls.get(activity_level, 1.2) # tdee

    # Calculate Calories Based on Goal
def adjust_calories(tdee, goal):
        if goal == "weight_loss":
            return tdee - 500
        elif goal == "weight_gain":
            return tdee + 500
        else:  # Maintenance
            return tdee
        
    # Macronutrient Distribution Ratios
def calculate_macros(calories, goal):
        if goal == "weight_loss":
            protein_ratio, fat_ratio, carb_ratio = 0.3, 0.3, 0.4
        elif goal == "weight_gain":
            protein_ratio, fat_ratio, carb_ratio = 0.25, 0.3, 0.45
        else:  #  maintenance
            protein_ratio, fat_ratio, carb_ratio = 0.3, 0.3, 0.4
        
        protein = (calories * protein_ratio) / 4
        fat = (calories * fat_ratio) / 9
        carbs = (calories * carb_ratio) / 4
        return protein, fat, carbs
    
@app.route('/')
def home():
    return render_template('web.html',Name='',
                           Calories='',
                           ProteinContent='',
                           FatContent='',
                           CarbohydrateContent='',
                           SodiumContent='',
                           Recipe='',
                           RecipeInstructions='',
                           l='')

@app.route('/recommend', methods=['POST'])
def recommend():
    
    # User inputs
    age = int(request.form['age'])
    sex = request.form['sex']
    weight = int(request.form['weight'])
    height = int(request.form['height'])
    activity_level = request.form['activity_level']
    goal = request.form['goal']
    diet_preference = request.form['diet_preference']
    # allergies = request.form['allergies']
    n = int(request.form['n'])
    
    user_profile = {}
    user_profile["age"] =age
    user_profile["sex"] =sex
    user_profile["weight"] =weight
    user_profile["height"] =height
    user_profile["activity_level"] =activity_level
    user_profile["goal"] =goal
    user_profile["diet_preference"] =diet_preference
    # user_profile["allergies"] =[allergies]
    
    # Compute User Nutritional Needs
    bmr = calculate_bmr(user_profile["weight"], user_profile["height"], user_profile["age"], user_profile["sex"])
    tdee = calculate_tdee(bmr, user_profile["activity_level"])
    target_calories = adjust_calories(tdee, user_profile["goal"])
    target_protein, target_fat, target_carbs = calculate_macros(target_calories, user_profile["goal"])
    
    # Filter Recipes Based on Diet Preferences
    filtered_diet = df.copy()
    if user_profile["diet_preference"] in ["vegetarian", "vegan"]:
        filtered_diet = filtered_diet[filtered_diet["RecipeInstructions"].str.contains(user_profile["diet_preference"], case=False, na=False)]

    # for allergen in user_profile["allergies"]:
    #     filtered_diet = filtered_diet[~filtered_diet["RecipeInstructions"].str.contains(allergen, case=False, na=False)]
        
    # Content-Based Recommendation Using Cosine Similarity
    def recommend_meals(user_calories, user_fat, user_carbs, user_protein, top_n):
        # User profile vector includes all 9 features, and we fill missing features with zeros (or use other defaults)
        user_profile_vector = np.array([[user_calories, user_fat, user_carbs, user_protein, 0, 0, 0, 0, 0]])
        
        # Compute Cosine Similarity
        similarities = cosine_similarity(user_profile_vector, filtered_diet.iloc[:, 1:10].values)  # Adjusting for 9 features
        
        # Rank meals based on similarity
        filtered_diet["Similarity"] = similarities[0]
        top_recommendations = filtered_diet.sort_values(by="Similarity", ascending=False).head(top_n)
        
        # Return recommendations in the desired format
        recommendations = []
        for _, row in top_recommendations.iterrows():
            recommendation = {
                "Name": row["Name"],
                "Calories": row["Calories"],
                "ProteinContent": row["ProteinContent"],
                "FatContent": row["FatContent"],
                "CarbohydrateContent": row["CarbohydrateContent"],
                "SodiumContent": row["SodiumContent"],
                "RecipeInstructions": row["RecipeInstructions"]
            }
            recommendations.append(recommendation)
        
        return recommendations
    
    # Get Recommendations
    recommendations = recommend_meals(target_calories, target_fat, target_carbs, target_protein,n)
    
    return render_template('web.html', recommendations=recommendations)

        
if __name__ == '__main__':
    app.run(debug=True)