from django.urls import path
from .views import restauranMain, addRestauran

urlpatterns = [
    path("Restauran", restauranMain),
    path("Reastauran/add/Restauran", addRestauran),

]