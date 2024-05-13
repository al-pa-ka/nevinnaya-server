from django.db import models

# Create your models here.


class Token(models.Model):
    token = models.CharField(max_length=200)
    exp_in = models.DateTimeField()
    user = models.OneToOneField('Admin', on_delete=models.CASCADE)

class User(models.Model):
    class Meta:
        abstract = True
    login = models.EmailField()
    password = models.CharField(max_length=30)
    

class Admin(User): ...
