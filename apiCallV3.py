#modifed version of code in this blog: (https://medium.com/@your_data_scientist_bestie/exploring-pythons-delicious-side-spoonacular-api-adventures-34af451262bc)
#also used some chatgpt to debug, but reformated by Theresa and Dora
#had help from Varun as well (bc we won speed cts!)

import requests
import json

class Recipe:
    def __init__(self, name, servings, prepTime, ingredients):
        self.name = name
        self.servings = servings
        self.prepTime = prepTime
        self.ingredients = ingredients
    
    def __repr__(self):
        return (f'{self.name}: {self.servings} servings, ' +
               f'{self.prepTime} mins of prep time, ' 
               f'and ingredients: {self.ingredients}')

class Ingredient:
    def __init__(self, name, metric, amount):
        self.name = name
        self.metric = metric
        self.amount = amount

    def __repr__(self):
        return f'{self.amount} {self.metric} of {self.name}'

# Query --> a list of arguments passed in by the user via button clicks
def callRecipe(query): 
    base_url = 'https://api.spoonacular.com/recipes/complexSearch'
    ingredients_url = 'https://api.spoonacular.com/recipes/{}/ingredientWidget.json'
    recipe_info_url = 'https://api.spoonacular.com/recipes/{}/information'
    api_key = 'e912d57b81fd4b0983f8c1b4ee3aad2f'

    # Search query parameters
    query_params = {
        # remember that query is a set
        'query': query,
        'number':5,
        'apiKey': api_key
    }

    # Fetch search results
    response = requests.get(base_url, params=query_params)
    response.raise_for_status()
    data = response.json()

    # Loop through the recipes
    recipes = data['results']
    for recipe in recipes:
        # Print the title of the recipe
        # print("Title:", recipe['title'])

        # Get recipe ID
        recipe_id = recipe['id']
        
        # Fetch detailed recipe information (e.g., servings, prep time)
        recipe_info_response = requests.get(recipe_info_url.format(recipe_id), params={'apiKey': api_key})
        recipe_info_response.raise_for_status()
        recipe_info_data = recipe_info_response.json()

        # Print additional information like servings and preparation time
        recipe_name = recipe_info_data['title']
        recipe_servings = recipe_info_data['servings']
        recipe_prep_time = (recipe_info_data['readyInMinutes'], "minutes")
        

        # print("Additional Information:")
        # print("Servings:", recipe_info_data['servings'])
        # print("Preparation Time:", recipe_info_data['readyInMinutes'], "minutes")

        # Fetch ingredients for the recipe from the ingredientWidget endpoint
        ingredients_response = requests.get(ingredients_url.format(recipe_id), params={'apiKey': api_key})
        ingredients_response.raise_for_status()
        ingredients_data = ingredients_response.json()

        # Print ingredients
        recipe_ingredients = []
        for ingredient in ingredients_data['ingredients']:
            ingredient_to_add = Ingredient(ingredient['name'], ingredient['amount']['us']['unit'], ingredient['amount']['us']['value'])
            recipe_ingredients.append(ingredient_to_add)
        
        final_recipe = Recipe(recipe_name, recipe_servings, recipe_prep_time[0], recipe_ingredients)
        return final_recipe


print(callRecipe({'apple','banana'}))
