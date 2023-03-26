import os
import openai
import json
import requests

from flask import Flask, render_template, request
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    gender = request.form['gender']
    age = request.form['age']
    location = request.form['location']
    preferences = request.form['preferences']
    # month = request.form['month']
    print("Name:", name)
    print("Gender:", gender)
    print("Age:", age)
    print("Location:", location)
    print("Preferences:", preferences)
    # print("Month:", month)
    mealplan = generate_meal_plan(name, gender, age, location, preferences)
    print(mealplan)

    data = mealplan["choices"][0]["text"].strip()
    with open('example_data2.json', 'w') as f:
        f.write(json.dumps(data))
        # f.write(data)

    # Call the function with an empty argument
    # flatfile = file_open()
    clean_json = parse_json(data)
    print(clean_json)
    with open('example_data3.json', 'w') as f:
        # f.write(json.dumps(data))
        f.write(clean_json)

    instacart = get_instacart_recipe()
    print(instacart)

    return render_template('submitted.html')





###### TO TRY
######## Instacart stuff from app_original.py
# Load the recipe options from the local file
# with open('example_data3.json', 'r') as f:
#     recipe_options = json.load(f)

# @app.route('/parse_ingredients', methods=['POST'])
# def parse_ingredients():
#     # Get the meal plan option from the request
#     data = json.loads(request.data)
#     meal_plan_option = data[0]['ingredients_chosen']

#     # Find the corresponding recipe list for the selected meal plan option
#     recipe_list = recipe_options[meal_plan_option]

#     # Extract the recipe names and ingredients for each recipe
#     recipes = []
#     for recipe in recipe_list:
#         recipe_name = recipe['meal_description']
#         ingredients = recipe['ingredients_chosen']
#         recipes.append({'title': recipe_name, 'ingredients': ingredients})

#     # Return the list of recipes with their ingredients
#     return json.dumps(recipes)

# # Endpoint to select the meal plan option
# @app.route('/select_meal_plan', methods=['GET'])
# def select_meal_plan():
#     # Return a list of available meal plan options
#     return json.dumps(list(recipe_options.keys()))



########
if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)



#######
def generate_meal_plan(name, gender, age, location, preferences):
    ingredients = 'Fruit, Citrus (grapefruit, kumquats, lemons, mandarins), Vegetables, Asparagus, Cabbage, Cauliflower, Kale, Pea shoots, Radish, Snow peas, Winter squash'
    custom_prompt=f"Your goal is to create a series of meal plan options for a user based on their age, gender, location, and\
       time of year (in order to account for seasonal ingredients right now), and dietary preferences\n\n\
       Here's the user data:\n\nLocation: {location}\n\
       Seasonal ingredients: {ingredients}\nGender: {gender}\nAge: {age}\nDietary Preferences: {preferences}\n\nUsing only the ingredients in season, general meal plan options as a JSON object with the following fields (meal_number, time_of_day, meal_description, ingredients_chosen, recipe_for_meal. For the \"recipe_for_meal\" do not provide a link, but generate a new recipe:",

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt = custom_prompt, 
        temperature=0.7,
        max_tokens=1938,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )
    # print(response)
    return response


# NO LONGER NEED
# def file_open():
#     # Open the file in read mode
#     with open('example_data2.json', 'r') as f:
#         # Read the contents of the file into the argument
#         argument = f.read()
    
#     # Do something with the argument
#     return(argument)


#parsing json and turning it into a format we want
def parse_json(data):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Format the following as valid JSON:{data}\n\n\n###",
    temperature=0.7,
    max_tokens=1438,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response["choices"][0]["text"].strip('\n')







# ###### TO TRY
# # feed output into Instacart
def get_instacart_recipe():
    # Load the recipe options from the local file
    with open('example_data3.json', 'r') as f:
        recipe_options = json.load(f)

    headers = {
        'User-Agent': 'ChatGPT-Agent',
        }

    parsed_json_meal_plan = recipe_options
    recipe_name = parsed_json_meal_plan[0]['meal_description']
    ingredients = parsed_json_meal_plan[0]['ingredients_chosen']
    # Create the POST request data
    post_data = {'title': recipe_name, 'ingredients': ingredients}
    # Make the POST request
    response = requests.post('https://www.instacart.com/v3/partner_recipe', json=post_data, headers=headers)
    print(post_data)
    # Return the response
    print(response.content)

    return json.loads(response.content)['url']

    





