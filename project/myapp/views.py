import json
import time
from datetime import datetime

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import RestauranTypes, Restauran, RestauranPhotos, Review, Owner, Employee
from .forms import RegistrationForm

# Create your views here.
@csrf_exempt
def restauranMain(request):
    if request.method == "GET":
        restaurans = Restauran()
        selected_types = request.GET.getlist("restaurantTypes")

        if selected_types:
            restaurans = Restauran.objects.filter(
                restauranType__id__in=selected_types
            ).distinct()
        else:
            restaurans = Restauran.objects.all()
        rTypes = RestauranTypes.objects.all()

        return render(request,"restaurant/main.html",
            {
                "restaurans": restaurans,
                "rTypes": rTypes
            }
        )

    elif request.method == "DELETE":
        data = json.loads(request.body)
        restaurant_id = data.get("id")
        restaurant = Restauran.objects.get(id=restaurant_id)
        restaurant.delete()
        return JsonResponse(
            {"message": "Restaurant deleted"},
            status=200
        )

@csrf_exempt
def editRestauran(request, id):
    restauran: Restauran = Restauran.objects.get(id=id)

    if request.method == "GET":
        rTypes = RestauranTypes.objects.all()
        owners = Owner.objects.all()
        return render(
            request,"restaurant/editRestauran.html",
            {
                "restauran": restauran,
                "rTypes": rTypes,
                "owners": owners,
            }
        )

    elif request.method == "POST":
        restauran.name = request.POST.get("name")
        restauran.adress = request.POST.get("adress")
        restauran.phoneNumber = request.POST.get("phoneNumber", "")
        restauran.website = request.POST.get("website")
        restauran.save()

        restauran.restauranType.set(request.POST.getlist("restauranType"))
        restauran.owner_set.set(request.POST.getlist("owners"))

        files = request.FILES.getlist('images')
        for file in files:
            if file:
                RestauranPhotos.objects.create(image=file, restauran=restauran)

        return redirect(f"/Restauran/{id}/")

@csrf_exempt
def addRestauran(request):
    if request.method == "GET":
        rTypes = RestauranTypes.objects.all()
        owners = Owner.objects.all()
        return render(request, "restaurant/addRestauran.html", {"rTypes": rTypes, "owners": owners})
    
    elif request.method == "POST":
        name: str = request.POST.get("name")
        adress: str = request.POST.get("adress")
        phoneNumber: str = request.POST.get("phoneNumber", "")
        website: str = request.POST.get("website")
        
        rst = Restauran.objects.create(
            name=name,
            adress=adress,
            phoneNumber=phoneNumber,
            website=website,
        )
        
        rst.restauranType.set(request.POST.getlist("restauranType"))
        rst.owner_set.set(request.POST.getlist("owners"))

        files = request.FILES.getlist('images')
        for file in files:
            if file:
                RestauranPhotos.objects.create(image=file, restauran=rst)

        return redirect(f"/Restauran/{rst.id}/")


def page_not_found(request, exception):
    return render(request, "notFound.html", {"title": "Page not found"})


def restauran_detail(request, id):
    restauran = get_object_or_404(Restauran, id=id)
    photos = RestauranPhotos.objects.filter(restauran=restauran)
    reviews = Review.objects.filter(restauran=restauran, isVisible=True).order_by("-created_at")
    employees = Employee.objects.filter(restaurant=restauran).order_by("surname", "name")
    return render(request, "restaurant/detail.html", {
        "restauran": restauran,
        "photos": photos,
        "reviews": reviews,
        "employees": employees,
    })


@csrf_exempt
def add_review(request, id):
    restauran = Restauran.objects.get(id=id)
    if request.method == "POST":
        data = json.loads(request.body)
        review_text = data.get("review", "")
        is_visible = request.user.is_authenticated
        Review.objects.create(
            review=review_text,
            restauran=restauran,
            user=request.user if request.user.is_authenticated else None,
            isVisible=is_visible
        )
        message = "Review added" if is_visible else "Review submitted and will be published after moderation"
        return JsonResponse({"message": message})
    return HttpResponseNotFound()


@csrf_exempt
def add_employee(request, id):
    restauran = get_object_or_404(Restauran, id=id)
    if request.method == "POST":
        data = json.loads(request.body)
        hiring_date = None
        date_str = data.get("dateOfHiring")
        if date_str:
            try:
                hiring_date = datetime.fromisoformat(date_str).date()
            except ValueError:
                hiring_date = None

        employee = Employee.objects.create(
            name=data.get("name", ""),
            surname=data.get("surname", ""),
            contactphone=data.get("contactphone", ""),
            email=data.get("email", ""),
            salary=int(data.get("salary") or 0),
            dateOfHiring=hiring_date or datetime.now().date(),
            restaurant=restauran,
        )
        return JsonResponse({"message": "Employee added", "employeeId": employee.id})
    return HttpResponseNotFound()


@csrf_exempt
def delete_employee(request, restauran_id, employee_id):
    if request.method == "DELETE":
        employee = get_object_or_404(Employee, id=employee_id, restaurant__id=restauran_id)
        employee.delete()
        return JsonResponse({"message": "Employee deleted"})
    return HttpResponseNotFound()


def owners_list(request):
    owners = Owner.objects.all().order_by("surname", "name")
    return render(request, "restaurant/owners.html", {"owners": owners})


def restaurant_employees(request, id):
    restauran = get_object_or_404(Restauran, id=id)
    employees = Employee.objects.filter(restaurant=restauran).order_by("surname", "name")
    return render(request, "restaurant/employees.html", {"restauran": restauran, "employees": employees})


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username") or f"user_{int(time.time())}"
            email = form.cleaned_data.get("email") or ""
            password = form.cleaned_data.get("password") or None
            original_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{original_username}_{counter}"
                counter += 1
            user = User.objects.create_user(username=username, email=email, password=password)
            auth_login(request, user)
            return redirect("restauran_main")
    else:
        form = RegistrationForm()
    return render(request, "restaurant/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("restauran_main")
    else:
        form = AuthenticationForm()
    return render(request, "restaurant/login.html", {"form": form})


def logout_view(request):
    auth_logout(request)
    return redirect("restauran_main")