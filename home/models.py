from django.db import models

# Create your models here.
class contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name + self.email
    
class Item(models.Model) :
    product_name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
