from django.db import models
from django.contrib.auth.models import User

class FoodCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Cuisine(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class FlavorProfile(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name
class TextureProfile(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=100, unique=True)
    food_types = models.ManyToManyField(FoodCategory, blank=True)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, null=True, blank=True)
    flavor_profile = models.ManyToManyField(FlavorProfile, blank=True);
    texture_profile = models.ManyToManyField(TextureProfile, blank=True);

    def __str__(self):
        return self.name

class Allergy(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class DietaryRequirement(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class HealthGoals(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class UserFoodSelection(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    liked_foods = models.ManyToManyField(Food, blank=True, related_name="liked_by_users")
    disliked_foods = models.ManyToManyField(Food, blank=True, related_name="disliked_by_users")
    allergy = models.ManyToManyField(Allergy, blank=True, related_name="user_allergy")
    dietary_requirement = models.ManyToManyField(DietaryRequirement, blank=True, related_name="user_dietary_requirement")
    health_goals = models.ManyToManyField(HealthGoals, blank=True, related_name="user_health_goal")
    def __str__(self):
        return f"{self.user.username}'s Food Preferences"
