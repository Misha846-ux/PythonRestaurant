from django.urls import path
from .views import (
    restauranMain,
    addRestauran,
    editRestauran,
    restauran_detail,
    add_review,
    register_view,
    login_view,
    logout_view,
)

urlpatterns = [
    path("", restauranMain, name="restauran_main"),
    path("Restauran", restauranMain),
    path("Reastauran/add/Restauran", addRestauran),
    path("Restauran/edit/<int:id>", editRestauran, name="edit_restauran"),
    path("Restauran/<int:id>/", restauran_detail, name="restauran_detail"),
    path("Restauran/<int:id>/add_review", add_review, name="add_review"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]