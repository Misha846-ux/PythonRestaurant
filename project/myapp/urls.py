from django.urls import path
from .views import restauranMain, addRestauran, editRestauran

urlpatterns = [
    path("Restauran", restauranMain),
    path("Reastauran/add/Restauran", addRestauran),
    path("Restauran/edit/<int:id>",editRestauran,name="edit_restauran"),

]