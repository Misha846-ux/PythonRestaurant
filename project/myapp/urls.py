from django.urls import path
from .views import restauranMain, addRestauran, editRestauran, restauran_detail, add_review

urlpatterns = [
    path("Restauran", restauranMain),
    path("Reastauran/add/Restauran", addRestauran),
    path("Restauran/edit/<int:id>", editRestauran, name="edit_restauran"),
    path("Restauran/<int:id>/", restauran_detail, name="restauran_detail"),
    path("Restauran/<int:id>/add_review", add_review, name="add_review"),
]