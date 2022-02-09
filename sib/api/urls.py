from django.urls import path

from .views import APIDeal

urlpatterns = [
    path('deals/', APIDeal.as_view()),
]
