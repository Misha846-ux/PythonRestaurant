from django.urls import path
from .views import (
    restauranMain,
    addRestauran,
    editRestauran,
    restauran_detail,
    add_review,
    add_employee,
    delete_employee,
    owners_list,
    restaurant_employees,
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
    path("Restauran/<int:id>/add_employee/", add_employee, name="add_employee"),
    path("Restauran/<int:restauran_id>/delete_employee/<int:employee_id>/", delete_employee, name="delete_employee"),
    path("Restauran/<int:id>/employees/", restaurant_employees, name="restaurant_employees"),
    path("owners/", owners_list, name="owners_list"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]