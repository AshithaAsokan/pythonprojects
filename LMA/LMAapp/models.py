from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class User_details(models.Model):
    User_Id =models.IntegerField( default='null')
    UserType = models.CharField(max_length=10 )
    UserName = models.CharField(max_length=10)
    Gender = models.CharField(max_length=10)
    DateofBirth = models.DateField()
    Address = models.CharField(max_length=30)
    PhoneNumber = models.IntegerField()
    EmailId = models.EmailField()

    def __str__(self):
        return self.UserName

class Book_details(models.Model):
    Book_Id =models.IntegerField(default=0)
    Book_Title = models.CharField(max_length=20)
    Author = models.CharField(max_length=10)
    Image = models.ImageField(upload_to='images/', blank=True, null=True)
    Publication = models.CharField(max_length=10)
    Edition = models.CharField(max_length=10)
    Price = models.IntegerField()
    Date = models.DateField()
    Quantity = models.PositiveIntegerField(default=0)
    Status = models.CharField(max_length=10)
  

class Res_fin_details(models.Model):
    UserName=  models.CharField(max_length=20)
    Book_Title =  models.CharField(max_length=20)
    Date_issue = models.DateField()
    Date_return = models.DateField()
    fine = models.IntegerField()
    status = models.CharField(max_length=10)

class Add_Bag(models.Model):
    Book_Title = models.CharField(max_length=20)
    UserName=models.CharField(max_length=20)
    AddDate = models.DateField()
    Datereturn = models.DateTimeField()
    def __str__(self):
        return f"{self.UserName}'s Bag: {self.Book_Title}"

class purchase(models.Model):
    Book_Title = models.CharField(max_length=20)
    UserName=models.CharField(max_length=20)
    AddDate = models.DateField()
    Datereturn = models.DateTimeField()
    status = models.CharField(max_length=10)
