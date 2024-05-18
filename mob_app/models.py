from django.db import models

# Create your models here.
class Users(models.Model):
    u_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=40)
    phone = models.CharField(max_length=20)
    email_id=models.CharField(max_length=20)
    password = models.CharField(max_length=30)
    age=models.CharField(max_length=30)
    gender=models.CharField(max_length=30)

class Mobiles(models.Model):
    m_id=models.IntegerField(primary_key=True)
    mobile_name=models.CharField(max_length=200)
    ram=models.CharField(max_length=200)
    rom=models.CharField(max_length=200)
    camera=models.CharField(max_length=200)
    size=models.CharField(max_length=200)
    battery=models.CharField(max_length=200)
    rating=models.CharField(max_length=200)
    price=models.CharField(max_length=200)
    picture=models.CharField(max_length=200)

class Purchase(models.Model):
    p_id=models.IntegerField(primary_key=True)
    u_id=models.IntegerField()
    mobile_name=models.CharField(max_length=200)
    rating=models.CharField(max_length=200)
    review=models.CharField(max_length=200)
