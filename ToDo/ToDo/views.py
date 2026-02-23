from django . shortcuts import render,redirect
from django.contrib.auth.models import User
from ToDo import models
from ToDo.models import TODO
from django.contrib import auth

def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        feml = request.POST.get('feml')
        fpwd = request.POST.get('fpwd')
        print(fnm, feml, fpwd)
        my_user=User.objects.create_user(fnm, feml, fpwd)
        my_user.save()
        return redirect('/login')

    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        fpwd = request.POST.get('fpwd')
        print(fnm, fpwd)

        user = auth.authenticate(request, username=fnm, password=fpwd)
        if user is not None:
            auth.login(request, user)
            return redirect('/todo')
        else:
            return redirect('/login')

    return render(request, 'login.html')

def todoapp(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        print(title)
        obj = models.TODO(title = title, user = request.user)
        obj.save()
        res = models.TODO.objects.filter(user = request.user).order_by('-date')
        return redirect('/todo', {'res':res})
    res = models.TODO.objects.filter(user = request.user).order_by('-date')
    return render(request, 'todo.html', {'res':res})

def delete_todo(request, serialno):
    obj = models.TODO.objects.get(serialno = serialno)
    obj.delete()
    return redirect('/todo')

def signout(request):
    auth.logout(request)
    return redirect('/login')
