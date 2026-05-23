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
def restauranMain(request):
    return render(request, "restaurant/main.html")

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
            rst.restauranType.add(RestauranTypes.objects.filter(id = el))
        return JsonResponse({"message": "Product created"})


def page_not_found(request, exception):
    return render(request, "notFound.html", {"title": "Page not found"})