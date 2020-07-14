from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth

# Create your views here.


def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            if request.POST['email'] and request.POST['password']:
                try:
                    user = User.objects.get(email=request.POST['email'])
                    auth.login(request, user)
                    if request.POST['next'] != '':
                        return redirect(request.POST['next'])
                    else:
                        return redirect('/')
                    return redirect('/')
                except User.DoesNotExist:
                    return render(request, 'login.html', {'error': "User Doesn't Exists"})
            else:
                return render(request, 'login.html', {'error': "Empty Field"})
        else:
            return render(request, 'login.html')
    else:
        return redirect('/')


def signup(request):
    if request.method == "POST":
        if request.POST['password'] == request.POST['password2']:
            if request.POST['username'] and request.POST['email'] and request.POST['password']:
                try:
                    user = User.objects.get(email=request.POST['email'])
                    return render(request, 'signup.html', {'error': "User already Exist!"})
                except User.DoesNotExist:
                    User.objects.create_user(
                        username=request.POST['username'],
                        email=request.POST['email'],
                        password=request.POST['password'],
                    )
                    messages.success(request, 'SignUp Successful!\nLogin Here')
                    return redirect(login)
            else:
                return render(request, 'signup.html', {'error': "Empty Field"})
        else:
            return render(request, 'signup.html', {'error': "Password's don't match"})
    else:
        return render(request, 'signup.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
