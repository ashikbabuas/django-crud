from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import ItemForm
from .models import Item
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'Item/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'Item/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentitem')
            except IntegrityError:
                return render(request, 'Item/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'Item/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'Item/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'Item/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currentitem')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def currentitem(request):
    items = Item.objects.filter(user=request.user)
    return render(request, 'Item/currentItem.html', {'items':items})

@login_required
def createitem(request):
    if request.method == 'GET':
        return render(request, 'Item/createItem.html', {'form':ItemForm()})
    else:
        try:
            form = ItemForm(request.POST)
            newitem = form.save(commit=False)
            newitem.user = request.user
            newitem.save()
            return redirect('currentitem')
        except ValueError:
            return render(request, 'Item/createItem.html', {'form':ItemForm(), 'error':'Bad data passed in. Try again.'})

@login_required
def viewitem(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk, user=request.user)
    if request.method == 'GET':
        form = ItemForm(instance=item)
        return render(request, 'item/viewitem.html', {'item':item, 'form':form})
    else:
        try:
            form = ItemForm(request.POST, instance=item)
            form.save()
            return redirect('currentitem')
        except ValueError:
            return render(request, 'Item/viewitem.html', {'item':item, 'form':form, 'error':'Bad info'})

@login_required
def deleteitem(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk, user=request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('currentitem')
