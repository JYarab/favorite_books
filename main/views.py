import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Book, User
import bcrypt
from datetime import datetime

# base route to login/reg page
def index(request):
    return render(request, 'index.html')

#registration user check/creation
def create_user(request):
    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    
    #no errors create new user
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

    new_user = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=(request.POST['email']).lower(),
        password=hashed_pw
        )
    request.session['logged_in_user'] = new_user.id
    return redirect('/books')

#user login check
def login(request):
    email=(request.POST['email']).lower()
    users = User.objects.filter(email=email)
    if users:
        logging_user = users[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logging_user.password.encode()):
            request.session['logged_in_user'] = logging_user.id
            return redirect('/books')
        else:
            messages.error(request, "Invalid email or password", extra_tags="login")
            return redirect('/')
    messages.error(request, "Invalid email", extra_tags="login")
    return redirect('/')

#logout
def logout(request):
    request.session.clear()
    return redirect('/')

#list of books and create book form
def books(request):
    if 'logged_in_user' in request.session:
        context = {
            'user': User.objects.get(id=request.session['logged_in_user']),
            'books' : Book.objects.all()
        }
        return render(request, 'books.html', context)
    
    return redirect('/')

#single book deatil page
def book_page(request, id):
    if 'logged_in_user' in request.session:
        context = {
            'user': User.objects.get(id=request.session['logged_in_user']),
            'book' : Book.objects.get(id=id)
        }
        return render(request, 'book_info.html', context)
    return redirect('/')

#render user favorite book page
def user_page(request, id):
    if 'logged_in_user' in request.session:
        context = {
            'user': User.objects.get(id=request.session['logged_in_user']),
        }
        return render(request, 'user_page.html', context)
    return redirect('/')

#validate and create new book
def create_book(request):
    if 'logged_in_user' in request.session:
        errors = Book.objects.basic_validator(request.POST)
        users = User.objects.filter(id=request.POST['user'])
        user = users[0]

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')

        new_book= Book.objects.create(
        title=request.POST['title'],
        description=request.POST['desc'],
        uploaded_by=User.objects.get(id=user.id),
        )
        new_book.favorited_by.set(User.objects.filter(id=user.id))
        return redirect('/books')
    return redirect('/')

#logged in user favorite or unfavrotie a book
def favorite_book(request, id):
    if 'logged_in_user' in request.session:
        user = User.objects.get(id=request.session['logged_in_user'])
        book = Book.objects.get(id=id)
        if user not in book.favorited_by.all():
            book.favorited_by.set(User.objects.filter(id=user.id))
        else:
            book.favorited_by.remove(User.objects.get(id=user.id))
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('/')

#uploader can edit a book
def edit_book(request, id):
    if 'logged_in_user' in request.session:
        errors = Book.objects.basic_validator(request.POST)
        book = Book.objects.get(id=id)
        
        #remove unique title error on edit if matches book being edited
        if 'title' in errors:
            if book.title == request.POST['title']:
                del errors['title']
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(request.META.get('HTTP_REFERER'))
        
        book.save()
        Book.objects.filter(id=id).update(title=request.POST['title'], description=request.POST['desc'])
        
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('/')

#uploader can delete a book
def delete_book(request, id):
    if 'logged_in_user' in request.session:
        Book.objects.filter(id=id).delete()
        return redirect('/books')
    return redirect('/')