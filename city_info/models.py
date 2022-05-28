from django.db import models


class City(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name


class Street(models.Model):
    name = models.CharField(max_length=30)
    city = models.ForeignKey('City', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
