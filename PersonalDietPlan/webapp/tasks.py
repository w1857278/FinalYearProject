from .models import *
from .services import *


def generate_prompt_task(user_id):
    user = User.objects.get(id=user_id)
    user_selection = UserFoodSelection.objects.get(user=user)
    recipe = GeneratedRecipe.objects.get(user=user)

    prompt = generate_prompt(user_selection)
    try:
        recipe.status = 'Generating'
        recipe.save()

        response = query_ollama(prompt)
        cleaned_response = clean_response(response)
        recipe.content = cleaned_response
        recipe.status = 'Completed'
        recipe.save()

    except Exception as e:
        recipe.status = f"Failed"
        recipe.content = str(e)
        recipe.save()