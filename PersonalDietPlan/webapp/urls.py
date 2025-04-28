from django.urls import path
from django.contrib.auth import views as auth_views
from webapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path("liked-foods/", views.liked_foods, name="liked_foods"),
    path("disliked-foods/", views.disliked_foods, name="disliked_foods"),
    path('allergy-dietary/', views.allergy_dietary, name='allergy_dietary'),
    path('health-goals/', views.health_goals, name='health_goals'),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("sign-up/", views.sign_up, name="sign_up"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path('waiting/', views.waiting, name='waiting'),
    path('response', views.response, name="response" ),
    path('check_status/', views.check_recipe_status, name='check_status'),
]
