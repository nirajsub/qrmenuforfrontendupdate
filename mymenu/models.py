from django.db import models
from django.contrib.auth.models import User
import uuid
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    uuid = models.UUIDField(default=uuid.uuid4, editable= False, null= False, unique= True, db_index= True)
    def __str__(self):
        return self.user.username

class Category(models.Model):
    user = models.ForeignKey(Admin, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="category", blank=True, null=True)
    not_available = models.BooleanField(default = False)
    def __str__(self):
        return self.name
    

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="product/")
    out_of_stock = models.BooleanField(default=False)
    todays_special = models.BooleanField(default=False)
    product_discount = models.IntegerField(blank=True, null=True)
    product_newprice = models.IntegerField(blank=True, null=True)
    exclusive = models.BooleanField(default=False)
    def __str__(self):
        return self.name
