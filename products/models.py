from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum  # Sum function
from .utils import Preference as Pref


# Create your models here.
class Product(models.Model):
    category = models.ForeignKey('Category', null=True,
                                 blank=True, on_delete=models.SET_NULL)
    subcategory = models.ForeignKey('Subcategory', null=True,
                                    blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, null=False, blank=False)
    short_desc = models.TextField()
    long_desc = models.TextField()
    color = models.CharField(max_length=50, null=False, blank=False) 
    sku = models.CharField(max_length=254, null=False, blank=False)
    brand = models.CharField(max_length=50, null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2,
                                null=False, blank=False)
    has_sizes = models.BooleanField(default=True, null=False, blank=False)
    image_url = models.URLField(null=False, blank=True)
    image = models.ImageField(max_length=1024, null=False, blank=True)
    style = models.CharField(max_length=15, choices=Pref.style_choices)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        """
        Update rating (based on the rating saved in Rating  model)
        """

        self.rating = self.ratings.aggregate(Sum('rating'))['rating__sum'] or 0

        self.save()

    def __str__(self):
        return self.name


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=50,
                            null=True, blank=False)
    friendly_name = models.CharField(max_length=50,
                                     null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Subcategory(models.Model):

    class Meta:
        verbose_name_plural = 'Subcategories'

    category = models.ForeignKey('Category', null=True,
                                 blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=40,
                            null=True, blank=False)
    friendly_name = models.CharField(max_length=40,
                                     null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_friendly_name_sub(self):
        return self.friendly_name


class Rating(models.Model):
    product = models.ForeignKey('Product', null=True,
                                blank=True, on_delete=models.CASCADE,
                                related_name="ratings")
    customer = models.ForeignKey(User, null=True,
                                 blank=True, on_delete=models.CASCADE,
                                 related_name="ratings")
    nickname = models.CharField(max_length=30, null=False, blank=False)
    rating = models.IntegerField(default=1)
    headline = models.CharField(max_length=150, null=False, blank=False)
    comment = models.TextField(max_length=1000, null=False, blank=True)
    recommend = models.CharField(max_length=3,
                                 choices=Pref.recommendation_choices)

    class Meta:
        unique_together = (('customer', 'product'),)

    def __str__(self):
        return f'Rating for {self.product.name} from order {self.customer}'
