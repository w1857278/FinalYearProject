import requests
import json
from collections import Counter
import re

def clean_response(response):
    cleaned = re.sub(r'<.*?>', '', response)
    cleaned = re.sub(r'#+\s*', '', cleaned)  
    cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)  
    return cleaned.strip()

OLLAMA_URL = "http://localhost:11434/api/generate"

def query_ollama(prompt, model="deepseek-r1:14b"):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True
    }

    response = requests.post(OLLAMA_URL, json=payload, stream=True)

    if response.status_code == 200:
        full_response = ""
        for line in response.iter_lines(decode_unicode=True):
            if line:
                try:
                    data = json.loads(line)
                    full_response += data.get("response", "")
                except json.JSONDecodeError as e:
                    full_response += f"\n[Invalid JSON chunk: {e}]"
        return full_response.strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

    


def generate_prompt(user_selection):
    liked_foods = user_selection.liked_foods.all()
    disliked_foods = user_selection.disliked_foods.all()

    liked = ", ".join([food.name for food in liked_foods]) or "None"
    disliked = ", ".join([food.name for food in disliked_foods]) or "None"
    allergies = ", ".join([a.name for a in user_selection.allergy.all()]) or "None"
    dietary = ", ".join([d.name for d in user_selection.dietary_requirement.all()]) or "None"
    goals = ", ".join([g.name for g in user_selection.health_goals.all()]) or "None"

    def count_profiles(foods, attr):
        profiles = []
        for food in foods:
            profiles.extend(getattr(food, attr).all())
        counter = Counter([p.name for p in profiles])
        return counter

    liked_flavor_counts = count_profiles(liked_foods, 'flavor_profile')
    disliked_flavor_counts = count_profiles(disliked_foods, 'flavor_profile')

    liked_texture_counts = count_profiles(liked_foods, 'texture_profile')
    disliked_texture_counts = count_profiles(disliked_foods, 'texture_profile')

    def format_counts(counts, label):
        if not counts:
            return f"No {label} found."
        return ". ".join([f"{name} appeared {count} times" for name, count in counts.items()])

    liked_flavors_summary = format_counts(liked_flavor_counts, "liked flavors")
    disliked_flavors_summary = format_counts(disliked_flavor_counts, "disliked flavors")

    liked_textures_summary = format_counts(liked_texture_counts, "liked textures")
    disliked_textures_summary = format_counts(disliked_texture_counts, "disliked textures")

    prompt = f"""
    Create a Diet plan for me according to the following:
    Likes: {liked}. 
    Dislikes: {disliked}. 
    Allergies: {allergies}.
    Dietary requirements: {dietary}.
    Health Goals: {goals}.

    Liked Flavours: {liked_flavors_summary}.
    Diskliked Flavours: {disliked_flavors_summary}.

    Liked Textures: {liked_textures_summary}.
    Disliked Textures: {disliked_textures_summary}.

    The plan should be health-focused, exclude allergens, align with my health goals, and include foods similar to what I like while avoiding foods similar to what I dislike.

    Please present the recipe in clean, natural, well-written paragraphs in plain text. Use second person perspective, addressing me as 'you' rather than 'the user'.  and avoid using any markdown, symbols, tags, or headings. Provide recipes with nutritional information sourced from the web.

    """

    return prompt.strip()

