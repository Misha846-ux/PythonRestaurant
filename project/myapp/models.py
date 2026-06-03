from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class RestauranTypes(models.Model):
    typeName = models.CharField(max_length=100)
    def __str__(self) -> str:
        return f"{self.id} {self.typeName}"

class Restauran(models.Model):
    name = models.CharField(max_length=50, blank=False)
    restauranType = models.ManyToManyField(RestauranTypes)
    adress = models.CharField(max_length=50, blank=False)
    phoneNumber = models.CharField(max_length=50)
    website = models.URLField(blank=False)
    def __str__(self) -> str:
        return f"{self.id} {self.name}"


class Review(models.Model):
    review = models.TextField(blank=False)
    created_at = models.DateField(auto_now=True)
    restauran = models.ForeignKey(Restauran, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    isVisible = models.BooleanField(default=True)

    def __str__(self) -> str:
        author = self.user.username if self.user else 'Anonymous'
        return f"{self.id} ({author}) {self.review[:40]}"

class RestauranPhotos(models.Model):
    image = models.ImageField(upload_to='restauran_photos/')
    restauran = models.ForeignKey(Restauran, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f"{self.id} {self.image.name}"

class Owner(models.Model):
    name = models.CharField(max_length=50, blank=False)
    surname = models.CharField(max_length=50, blank=False)
    contactphone = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=50)
    restaurants = models.ManyToManyField(Restauran)
    def __str__(self) -> str:
        return f"{self.id} {self.name}"

class Employee(models.Model):
    name = models.CharField(max_length=50, blank=False)
    surname = models.CharField(max_length=50, blank=False)
    contactphone = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=50)
    restaurant = models.ForeignKey(Restauran, on_delete=models.CASCADE)
    salary = models.IntegerField(blank=False)
    dateOfHiring = models.DateField(blank=False)
    def __str__(self) -> str:
        return f"{self.id} {self.name}"