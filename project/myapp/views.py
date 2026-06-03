from django.core.checks import templates
from django.http import HttpResponse, HttpResponseNotFound
from typing import Dict, Union
import json
from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from datetime import datetime

from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.conf import settings
import os

from .models import RestauranTypes, Restauran, RestauranPhotos, Review

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
    restauran = Restauran.objects.get(id=id)

    if request.method == "GET":
        rTypes = RestauranTypes.objects.all()
        return render(
            request,
            "restaurant/editRestauran.html",
            {
                "restauran": restauran,
                "rTypes": rTypes
            }
        )

    elif request.method == "POST":
        restauran.name = request.POST.get("name")
        restauran.adress = request.POST.get("adress")
        restauran.phoneNumber = request.POST.get("phoneNumber", "")
        restauran.website = request.POST.get("website")
        restauran.save()

        restauran.restauranType.set(request.POST.getlist("restauranType"))

        # handle uploaded photos
        files = request.FILES.getlist('images')
        for file in files:
            if file:
                RestauranPhotos.objects.create(image=file, restauran=restauran)

        return redirect(f"/Restauran/{id}/")

@csrf_exempt
def addRestauran(request):
    if request.method == "GET":
        rTypes = RestauranTypes.objects.all()
        return render(request, "restaurant/addRestauran.html", {"rTypes": rTypes})
    
    elif request.method == "POST":
        name = request.POST.get("name")
        adress = request.POST.get("adress")
        phoneNumber = request.POST.get("phoneNumber", "")
        website = request.POST.get("website")
        
        rst = Restauran.objects.create(
            name=name,
            adress=adress,
            phoneNumber=phoneNumber,
            website=website,
        )
        
        for el in request.POST.getlist("restauranType"):
            rst.restauranType.add(el)

        # handle uploaded photos
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
    reviews = Review.objects.filter(restauran=restauran).order_by("-created_at")
    return render(request, "restaurant/detail.html", {"restauran": restauran, "photos": photos, "reviews": reviews})


@csrf_exempt
def add_review(request, id):
    restauran = Restauran.objects.get(id=id)
    if request.method == "POST":
        data = json.loads(request.body)
        review_text = data.get("review")
        if review_text and review_text.strip():
            Review.objects.create(
                review=review_text.strip(),
                restauran=restauran
            )
        return JsonResponse({
            "message": "review added"
        })
    return HttpResponseNotFound()