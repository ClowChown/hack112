#modifed version of code in this blog: (https://medium.com/@your_data_scientist_bestie/exploring-pythons-delicious-side-spoonacular-api-adventures-34af451262bc)
#also used some chatgpt
import requests
import json

# Query --> a list of arguments passed in by the user via button clicks
def callRecipe(query): 
    base_url = 'https://api.spoonacular.com/recipes/complexSearch'
    ingredients_url = 'https://api.spoonacular.com/recipes/{}/ingredientWidget.json'
    recipe_info_url = 'https://api.spoonacular.com/recipes/{}/information'
    api_key = 'e912d57b81fd4b0983f8c1b4ee3aad2f'

    # Search query parameters
    query_params = {
        'query': {'apple','flour'},
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
        print("Title:", recipe['title'])

        # Get recipe ID
        recipe_id = recipe['id']
        
        # Fetch detailed recipe information (e.g., servings, prep time)
        recipe_info_response = requests.get(recipe_info_url.format(recipe_id), params={'apiKey': api_key})
        recipe_info_response.raise_for_status()
        recipe_info_data = recipe_info_response.json()

        # Print additional information like servings and preparation time
        print("Additional Information:")
        print("Servings:", recipe_info_data['servings'])
        print("Preparation Time:", recipe_info_data['readyInMinutes'], "minutes")

        # Fetch ingredients for the recipe from the ingredientWidget endpoint
        ingredients_response = requests.get(ingredients_url.format(recipe_id), params={'apiKey': api_key})
        ingredients_response.raise_for_status()
        ingredients_data = ingredients_response.json()

        # Print ingredients
        print("Ingredients:")
        for ingredient in ingredients_data['ingredients']:
            print(f"{ingredient['name']} - {ingredient['amount']}")

        # Print a separator for readability
        print("\n" + "="*50 + "\n")

    