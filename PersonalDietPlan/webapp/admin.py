from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(FoodCategory)
admin.site.register(Cuisine)
admin.site.register(Food)
admin.site.register(UserFoodSelection)
admin.site.register(Allergy)
admin.site.register(DietaryRequirement)
admin.site.register(HealthGoals)
admin.site.register(FlavorProfile)
admin.site.register(TextureProfile)