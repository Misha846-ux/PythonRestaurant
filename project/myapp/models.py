from django.db import models

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
    isVisible = models.BooleanField(default=True)
    def __str__(self) -> str:
        return f"{self.id} {self.review}"

class RestauranPhotos(models.Model):
    photoName = models.CharField(max_length=50, blank=False)
    restauran = models.ForeignKey(Restauran, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f"{self.id} {self.photoName}"
