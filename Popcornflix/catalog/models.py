from django.db import models
from django.contrib.auth.models import User

class House(models.Model):
    address = models.CharField(max_length=255)
    rooms = models.IntegerField()
    area = models.FloatField()
    floor = models.IntegerField()
    floor_number = models.IntegerField()
    price = models.FloatField()
    description = models.TextField()
    picture = models.ImageField(null=True, blank=True)
    liked_users = models.ManyToManyField(User, related_name='liked_users_house_set')
    auction = models.ManyToManyField(User, through='Auction', related_name='auction_house_set')

    def __str__(self):
        return f'{self.address} этаж: {self.floor} комнат: {"Студия" if self.rooms == 0 else self.rooms}'


class Auction(models.Model):
    rate = models.FloatField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='auction_user_set')
    house = models.ForeignKey(House, null=True, on_delete=models.CASCADE, related_name='auction_house_set')

    def __str__(self):
        return f'{self.user.username}: {self.rate} - {self.house.address}'






