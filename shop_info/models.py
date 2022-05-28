from django.db import models
from django.core.validators import MinValueValidator

import datetime
from pytz import timezone

from city_info.models import City, Street


class Shop(models.Model):
    name = models.CharField(max_length=30)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    street = models.ForeignKey(Street, on_delete=models.CASCADE)
    house_number = models.IntegerField(validators=[MinValueValidator(1)])
    open_time = models.TimeField()
    close_time = models.TimeField()

    def __str__(self):
        return self.name

    @staticmethod
    def get_current_time() -> datetime.time:
        current_datetime = datetime.datetime.now(tz=timezone('Europe/Moscow'))
        current_time = datetime.time(
            current_datetime.hour,
            current_datetime.minute,
            current_datetime.second
        )
        return current_time
