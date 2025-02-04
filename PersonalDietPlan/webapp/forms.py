from django import forms
from .models import *


class AllergyDietaryForm(forms.ModelForm):
    allergy = forms.ModelMultipleChoiceField(
        queryset=Allergy.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    dietary_requirement = forms.ModelMultipleChoiceField(
        queryset=DietaryRequirement.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = UserFoodSelection
        fields = ['allergy', 'dietary_requirement']


class HealthGoalsForm(forms.ModelForm):
    health_goals = forms.ModelMultipleChoiceField(
        queryset=HealthGoals.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = UserFoodSelection
        fields = ['health_goals']
