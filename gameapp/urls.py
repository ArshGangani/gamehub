from django.urls import path

from gameapp import views
app_name = "gameapp"


urlpatterns = [
    path("room", views.room, name="gameroom"),
    path('profile/<str:username>/', views.profile_stats, name='profile_stats')
]