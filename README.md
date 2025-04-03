# Diet Recommendation System Project Documentation

## Introduction
The Diet Recommendation System is a web-based application designed to provide personalized diet plans based on user inputs such as age, gender, weight, height, activity level, fitness goals, and dietary preferences. Built using Python’s Flask framework, the system leverages a large dataset of food items and recipes to recommend meals that align with the user’s nutritional needs, calculated using established formulas like the Mifflin-St Jeor equation for Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE). Cosine similarity is employed to match user nutritional profiles with suitable recipes from the dataset.

## Problem Statement
In today’s fast-paced world, individuals struggle to maintain a balanced diet that aligns with their unique nutritional needs, fitness goals, and dietary preferences. With an overwhelming amount of food and recipe information available, making informed meal choices is time-consuming and complex, especially for those without expertise in nutrition. Existing solutions often lack personalization, fail to account for diverse factors such as activity levels or specific dietary restrictions (e.g., vegetarianism), and do not efficiently process large datasets to deliver tailored recommendations in real time.
The challenge lies in developing a system that:
1.	Accurately calculates an individual’s nutritional requirements based on physiological data (age, sex, weight, height) and lifestyle factors (activity level, fitness goals).
2.	Filters and matches a vast dataset of over 500,000 recipes to user preferences and nutritional targets, while ensuring computational efficiency.
3.	Provides an accessible, user-friendly interface to simplify the process of meal planning.
Without such a system, users risk adopting diets that are either ineffective for their goals or incompatible with their preferences, leading to frustration and poor health outcomes. The Diet Recommendation System addresses this gap by leveraging data-driven calculations and content-based filtering to deliver personalized, practical, and preference-aligned meal suggestions.

## Objectives
•	Calculate personalized nutritional requirements (calories, protein, fat, carbs) based on user inputs.

•	Filter recipes according to dietary preferences (vegetarian, non-vegetarian).

•	Recommend top-N meals that best match the user’s nutritional goals using content-based filtering.

•	Provide an intuitive web interface for users to input data and view recommendations.

## Tools and Technologies
•	**Programming Language**: Python

•	**Web Framework**: Flask

•	**Frontend**: HTML, CSS for styling

•	**Libraries**: NumPy, Pandas, Scikit-learn (cosine similarity)

•	**Dataset**: columns [Name, Calories, FatContent, SaturatedFatContent, CholesterolContent, SodiumContent, CarbohydrateContent, FiberContent, SugarContent, ProteinContent, RecipeInstructions ] from the dataset:
https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews
________________________________________
## Problem-Solving Approach
The project addresses these challenges through a combination of data preprocessing, algorithmic efficiency, and modular design:

•	**Data Preprocessing**: Cleaned text fields (Name and RecipeInstructions) to remove special characters, extra spaces, and inconsistent formatting.

•	**Nutritional Calculations**: Implemented the Mifflin-St Jeor formula for BMR, adjusted for activity levels (TDEE), and applied goal-based calorie adjustments (e.g., ±500 kcal for weight loss/gain).

•	**Recommendation Engine**: Used cosine similarity to compare user nutritional profiles with recipe nutritional content, ensuring relevant meal suggestions.

•	**Web Interface**: Developed a Flask-based application with a clean HTML/CSS frontend, optimized for both desktop and mobile users.

•	**Efficiency**: Filtered the dataset based on dietary preferences before applying similarity calculations to reduce computational load.
________________________________________
## System Design
**Architecture**

  •	**Frontend**: A single-page HTML form (web.html) styled with CSS (style.css) for user input and result display.
  
  •	**Backend**: Flask application (app.py) handling request processing, nutritional calculations, and recommendation generation.
  
  •	**Data Layer**: Pandas DataFrame loaded from food.csv for in-memory data manipulation.

**Workflow**

1.	**User Input**: Collects age, sex, weight, height, activity level, goal, diet preference, and number of recommendations (n) via a POST request.
2.	**Nutritional Needs Calculation**:
   
      o	Compute BMR using the Mifflin-St Jeor formula.
      
      o	Calculate TDEE based on activity level multipliers.
      
      o	Adjust calories based on the user’s goal (weight loss, gain, or maintenance).
      
      o	Distribute calories into macronutrients (protein, fat, carbs) using predefined ratios.

3.	**Recipe Filtering**: Filter the dataset based on dietary preferences (e.g., vegetarian recipes).
4.	**Recommendation Generation**: Use cosine similarity to rank recipes by nutritional similarity to the user’s profile and return the top-N results.
5.	**Output**: Render recommendations in the HTML template with meal details (name, calories, macros, instructions).

## Key Algorithms
•	**Mifflin-St Jeor Formula**: 

    o	Male: BMR = (9.99 × weight) + (6.25 × height) - (4.92 × age) + 5
    
    o	Female: BMR = (9.99 × weight) + (6.25 × height) - (4.92 × age) - 161

•	**Cosine Similarity**: Measures the cosine of the angle between the user’s nutritional vector (calories, fat, carbs, protein) and each recipe’s nutritional vector.
________________________________________
## Implementation Details
**Code Structure**

•	**app.py**: 

    o	Flask app initialization and routing (/ for home, /recommend for processing).
    
    o	Data loading and preprocessing functions (preprocess_text, clean_instructions).
    
    o	Nutritional calculation functions (calculate_bmr, calculate_tdee, adjust_calories, calculate_macros).
    
    o	Recommendation logic (recommend_meals).

•	**web.html**:

    o	Form for user input with fields for all required parameters.
    
    o	Dynamic rendering of recommendations using Jinja2 templating.

•	**style.css**: 

    o	Responsive design with a food-themed background, centered containers, and styled inputs & buttons.

## Dataset Preprocessing
•	**Name Column**: Removed special characters and normalized whitespace.

•	**RecipeInstructions**: Stripped leading/trailing quotes and punctuation for consistent filtering.
________________________________________
## 📂 Project Structure
```
📦 Diet Recommendation System
├── 📂 app.py         # Contains Flask application logic and database models
├── 📂 viewdatabase.py     # Python file to view database
templates/
├── 📂 web.html
static/
├── 📂 style.css


├── 📜 LICENSE           # License file
├── 📜 README.md         # Project Documentation
```
________________________________________
## Problem Solving and Optimizations
**Challenge: Slow Recommendation Generation**

  •	**Problem**: Cosine similarity on 522,517 rows was computationally expensive.
  
  •	**Solution**: Applied dietary preference filtering first to reduce the dataset size before similarity calculations, improving response time.

**Challenge: Inconsistent Dataset Formatting**

  •	**Problem**: Special characters and irregular spacing in text fields caused filtering errors.
  
  •	**Solution**: Implemented preprocess_text and clean_instructions functions to standardize text data.

**Challenge: Limited Dietary Preference Support**

  •	**Problem**: Initial filtering only supported vegetarian/vegan preferences.
  
  •	**Solution**: Designed the system to be extensible—future enhancements could include keyword-based filtering for other diets (e.g., keto, gluten-free).
________________________________________
## Results and Evaluation
**Achievements**

  •	Successfully delivers personalized meal recommendations based on user inputs.
  
  •	Handles a large dataset with reasonable performance after optimizations.
  
  •	Provides a clean, visually appealing interface with clear recipe details.

**Limitations**

  •	Lacks support for allergies (commented out in code due to complexity).
  
  •	Assumes all nutritional data in food.csv is accurate and complete.
  
  •	No caching mechanism for repeated queries, which could further improve speed.

**Future Enhancements**

  •	Add allergy filtering by parsing ingredients in RecipeInstructions.
  
  •	Implement caching (e.g., using Redis) for faster repeat queries.
  
  •	Expand dietary preferences with more options and advanced text analysis.
  
  •	Show images of recipes.
________________________________________
## Conclusion
The Diet Recommendation System is a functional and user-friendly tool that demonstrates the application of nutritional science, machine learning (cosine similarity), and web development. By addressing challenges like dataset size, text preprocessing, and responsiveness, the project provides a solid foundation for further development. It serves as an excellent portfolio piece, showcasing skills in Python, Flask, data processing, and UI design.
________________________________________
## 🚀 Installation & Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/MuhammedAjmal786/Diet-Recommendation.git
   cd Diet-Recommendation
   ```

2. Install dependencies:
   ```bash
   pip install flask
   ```

3. Run the applications:
   - **Flask App**:
     ```bash
     cd app.py
     python app.py
     ```
________________________________________
## 🤝 Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## THANK YOU
