import os
import openai
import json
import requests

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_meal_plan(data):
  name = 'Katie'
  gender = 'Female'
  age = '23'
  location = 'Texas'
  preferences = 'likes chicken'
  # month = 'March'
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

  print(response)

  # data = response["choices"][0]["text"].strip()
  # with open('example_data2.json', 'w') as f:
  #     f.write(json.dumps(data))


# prompt chain
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


# feed output into Instacart
def get_instacart_recipe():
    # Load the recipe options from the local file
  with open('example_data.json', 'r') as f:
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

# mealplan = generate_meal_plan()
# print(mealplan)
# parsed_data = parse_json(generate_meal_plan)
# print(parsed_data)
instacart = get_instacart_recipe()
print(instacart)


