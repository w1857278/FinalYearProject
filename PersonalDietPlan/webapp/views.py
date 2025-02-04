from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Food, UserFoodSelection, FoodCategory, Cuisine

def home(request):
    return render(request, 'home.html')

@login_required
def liked_foods(request):
    foods = Food.objects.all()
    categories = FoodCategory.objects.all()
    cuisines = Cuisine.objects.all()
    user_selection, created = UserFoodSelection.objects.get_or_create(user=request.user)

    food_type = request.GET.get("filter_type")
    cuisine = request.GET.get("filter_cuisine")

    if food_type:
        foods = foods.filter(food_type__name=food_type)
    if cuisine:
        foods = foods.filter(cuisine__name=cuisine)

    if request.method == "POST":
        selected_food_ids = request.POST.getlist("foods")
        user_selection.liked_foods.set(selected_food_ids)
        return redirect("disliked_foods")

    return render(request, "liked_foods.html", {
        "foods": foods,
        "user_selection": user_selection,
        "categories": categories,
        "cuisines": cuisines
    })

@login_required
def disliked_foods(request):
    foods = Food.objects.all()
    categories = FoodCategory.objects.all()
    cuisines = Cuisine.objects.all()
    user_selection, created = UserFoodSelection.objects.get_or_create(user=request.user)

    food_type = request.GET.get("filter_type")
    cuisine = request.GET.get("filter_cuisine")

    if food_type:
        foods = foods.filter(food_type__name=food_type)
    if cuisine:
        foods = foods.filter(cuisine__name=cuisine)

    if request.method == "POST":
        selected_food_ids = request.POST.getlist("foods")
        user_selection.disliked_foods.set(selected_food_ids)
        return redirect("allergy_dietary")  

    return render(request, "disliked_foods.html", {
        "foods": foods,
        "user_selection": user_selection,
        "categories": categories,
        "cuisines": cuisines
    })

from django.shortcuts import render, redirect
from .forms import AllergyDietaryForm, HealthGoalsForm
from django.contrib.auth.decorators import login_required

@login_required
def allergy_dietary(request):
    user_food_selection, created = UserFoodSelection.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = AllergyDietaryForm(request.POST, instance=user_food_selection)
        if form.is_valid():
            form.save() 
            return redirect('health_goals') 
    else:
        form = AllergyDietaryForm(instance=user_food_selection)

    return render(request, 'allergy_dietary.html', {'form': form})

@login_required
def health_goals(request):
    user_food_selection, created = UserFoodSelection.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = HealthGoalsForm(request.POST, instance=user_food_selection)
        if form.is_valid():
            user_food_selection.user = request.user
            form.save()  
            return redirect('home')
    else:
        form = HealthGoalsForm(instance=user_food_selection)

    return render(request, 'health_goals.html', {'form': form})

