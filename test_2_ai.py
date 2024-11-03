import requests


api_key = "9771b891aac744468cfd200a710fa6a3"
print(requests.get("https://api.spoonacular.com/recipes/findByIngredients?ingredients=apples,+flour,+sugar&number=2&apiKey ={api_key}"))