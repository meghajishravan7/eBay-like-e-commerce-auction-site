from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Bid(models.Model):
    bid = models.FloatField(default=0)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='userbid')

    def __str__(self):
        return f'{self.bid}'


class Listing(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=500)
    image_url = models.CharField(max_length=1000)
    bid_price = models.ForeignKey(
        Bid, on_delete=models.CASCADE, blank=True, null=True, related_name='bidprice')
    isactive = models.BooleanField(default=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='user')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True, related_name='category')
    watchlist = models.ManyToManyField(
        User, blank=True, null=True, related_name='listingwatchlist')

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='usercomment')
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, blank=True, null=True, related_name='listingcomment')
    message = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.author} comment on {self.listing}'
