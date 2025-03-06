import openai
import os
from openai.error import RateLimitError, InvalidRequestError
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
else:
    print(f"API key found: {api_key[:5]}...")  # Print the first few characters for verification

openai.api_key = api_key

# Fetch scraped items from the Flask server
response = requests.get('http://127.0.0.1:5000/scraped_items')

if response.status_code == 200:
    scraped_items = response.json()
    # Convert the queried data to a list of tuples
    scraped_tuples = [(item['name'], item['discount']) for item in scraped_items]

    # Decide how many sale items to include in recipe
    selected_items = scraped_tuples

    prompt = f"Create three recipes using five ingredients from this data: {selected_items}. Assume the cook has basic ingredients like salt, pepper, butter, oil, etc. Do not use more than two meats for one recipe. Make sure to highlight the items from the tuples. The recipe should include a title, ingredients, and steps. Do not reuse ingredients among recipes"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        recipes_text = response.choices[0].message['content']
        print(recipes_text)

        # Split the response into individual recipes
        recipes = recipes_text.split("\n\nRecipe ")

        formatted_recipes = []
        for recipe_text in recipes:
            parts = recipe_text.split("\n\n")
            if len(parts) >= 3:
                title = parts[0].strip()
                ingredients = parts[1].strip().split("\n")
                steps = parts[2].strip().split("\n")

                formatted_recipe = {
                    "title": title,
                    "ingredients": {
                        "subheading": "Ingredients:",
                        "items": [ingredient.strip() for ingredient in ingredients]
                    },
                    "steps": {
                        "subheading": "Steps:",
                        "items": [step.strip() for step in steps]
                    }
                }

                # Format the recipe data to match the Recipe model
                recipe_data = {
                    "title": formatted_recipe["title"],
                    "ingredients": "\n".join(formatted_recipe["ingredients"]["items"]),
                    "steps": "\n".join(formatted_recipe["steps"]["items"])
                }

                formatted_recipes.append(recipe_data)

        # Print the formatted recipes data
        print("Formatted Recipes Data:")
        print(json.dumps(formatted_recipes, indent=4))

        # Post the recipes to the Flask server
        post_response = requests.post('http://127.0.0.1:5000/recipes', json=formatted_recipes)

        if post_response.status_code == 201:
            print("Recipes have been saved to the database.")
        else:
            print(f"Failed to save the recipes to the database. Status code: {post_response.status_code}")
    except RateLimitError:
        print("You exceeded your current quota. Please check your plan and billing details.")
    except InvalidRequestError as e:
        print(f"Invalid request: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
else:
    print(f"Failed to fetch scraped items. Status code: {response.status_code}")