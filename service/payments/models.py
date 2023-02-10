from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()

    def get_display_price(self):
        return f'{self.price / 100:02}'
