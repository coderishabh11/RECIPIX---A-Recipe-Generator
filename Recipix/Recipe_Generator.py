import requests

from config import API_KEY

def generate_recipe_from_ingredients(ingredient_list):
    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    params = {
        'apiKey': API_KEY,
        'ingredients': ','.join(ingredient_list),
        'number': 10,
        'ranking': 1,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        recipes = response.json()

        result = []
        for recipe in recipes:
            recipe_id = recipe['id']
            recipe_info_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
            recipe_info_params = {'apiKey': API_KEY}
            
            recipe_info_response = requests.get(recipe_info_url, params=recipe_info_params)
            
            if recipe_info_response.status_code == 200:
                recipe_info = recipe_info_response.json()
                result.append({
                    "Recipe ID": recipe_info['id'],
                    "Recipe Title": recipe_info['title'],
                    "Used Ingredients": [ingredient['name'] for ingredient in recipe['usedIngredients']],
                    "Instructions": recipe_info.get('instructions', 'Instructions not available')
                })

        return result

    return []

