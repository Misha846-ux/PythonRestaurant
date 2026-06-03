from django.core.checks import templates
from django.http import HttpResponse, HttpResponseNotFound
from typing import Dict, Union
import json
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from datetime import datetime

from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from .models import RestauranTypes, Restauran
from django.shortcuts import render

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

        body = json.loads(request.body)

        restauran.name = body["name"]
        restauran.adress = body["adress"]
        restauran.phoneNumber = body["phoneNumber"]
        restauran.website = body["website"]

        restauran.save()

        restauran.restauranType.set(
            body["restauranType"]
        )

        return JsonResponse({
            "message": "updated"
        })

@csrf_exempt
def addRestauran(request):
    if(request.method == "GET"):
        rTypes = RestauranTypes.objects.all()
        return render(request, "restaurant/addRestauran.html", {"rTypes": rTypes})
    elif (request.method == "POST"):
        body = json.loads(request.body)
        rst = Restauran.objects.create(
            name = body.get("name"),
            adress = body.get("adress"),
            phoneNumber = body.get("phoneNumber"),
            website = body.get("website"),
        )

        for el in body.get("restauranType"):
            rst.restauranType.add(el)
        return JsonResponse({"message": "Product created"})


def page_not_found(request, exception):
    return render(request, "notFound.html", {"title": "Page not found"})