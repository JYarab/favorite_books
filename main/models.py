from django.db import models
from django.db.models.fields import DateTimeField
from datetime import datetime
import re

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        users = User.objects.all()
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name must be at least 2 charaters'        
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 charaters'        
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invaild email address'
        else:
            for user in users:
                if postData['email'] == user.email:
                    errors['email'] = 'Email already in use'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 charaters'
        else:
            if postData['password'] != postData['conf_pass']:
                errors['password'] = "Passwords do not match"
        return errors

class BookManager(models.Manager):
    def basic_validator(self, postData):
        books = Book.objects.all()
        errors = {}
        
        if len(postData['title']) == 0:
            errors['title'] = 'Book title required'
        else:
            for book in books:
                if postData['title'] == book.title:
                    errors['title'] = 'Title must be unique'
        if len(postData['desc']) < 5:
            errors['desc'] = 'Description must be at least 5 characters long'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    #liked_books
    #books_uploaded
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name="liked_books")
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = BookManager()