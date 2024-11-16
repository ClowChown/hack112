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
        if self.servings == 1:
            servingMessage = 'serving'
        else:
            servingMessage = 'servings'
        return (f'{self.name}: {self.servings} {servingMessage} and ' +
               f'{self.prepTime} mins of prep time ' 
               f'with ingredients: {self.ingredients}')

class Ingredient:
    def __init__(self, name, metric, amount):
        self.name = name
        self.metric = metric
        self.amount = amount

    def __repr__(self):
        if self.metric == '':
            message = f'{self.amount} {self.name}'
            if self.amount == 1 and message[-1] == 's':
                message[:-1]
            elif self.amount != 1 and message[-1] != 's':
                message += 's'
            return message
        else:
            if self.amount == 1 and self.metric[-1] == 's':
                metric = self.metric[:-1]
            elif self.amount != 1 and self.metric[-1] != 's':
                metric = self.metric + 's'
            else:
                metric = self.metric
            return f'{self.amount} {metric} of {self.name}'

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
        'ignorePantry':True,
        'apiKey': api_key
    }

    # Fetch search results
    response = requests.get(base_url, params=query_params)
    response.raise_for_status()
    data = response.json()

    # Loop through the recipes
    recipes = data['results']
    for recipe in recipes:
        recipe_id = recipe['id']
        
        # Fetch detailed recipe information (e.g., servings, prep time)
        recipe_info_response = requests.get(recipe_info_url.format(recipe_id), params={'apiKey': api_key})
        recipe_info_response.raise_for_status()
        recipe_info_data = recipe_info_response.json()

        # Print additional information like servings and preparation time
        recipe_name = recipe_info_data['title']
        recipe_servings = recipe_info_data['servings']
        recipe_prep_time = (recipe_info_data['readyInMinutes'], "minutes")

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


print(callRecipe({'chocolate_chips','banana'}))
