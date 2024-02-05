from datetime import date
from django.db import models

# Create your models here.

class Customer(models.Model):
    first_name = models.CharField(max_length =  20)
    last_name =  models.CharField(max_length =  20)
    email =  models.CharField(max_length =  50)
    mobile = models.BigIntegerField(default = 0)
    gender = models.CharField(max_length = 10)
    city = models.CharField(max_length = 20)
    country = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)
    is_password_changed = models.BooleanField(default = False)
    last_changed_on = models.DateField(default = date.today)

    class Meta:
        db_table = 'customer_tb'
