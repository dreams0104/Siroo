from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import auth

# Create your views here.

User = get_user_model()

def sign_up(request):
    context = {}
    
    #POST Method
    if request.method == 'POST':
        if (request.POST['email'] and
                request.POST['password'] and
                request.POST['password'] == request.POST['password_check']):

            new_user = User.objects.create_user(
                email=request.POST['email'],
                name=request.POST['name'],
                nickname=request.POST['nickname'],
                gender=request.POST['gender'],
                password=request.POST['password'],
            )

            auth.login(request, new_user)
            return redirect('posts:index')
    
        else:
            context['error'] = '아이디와 비밀번호를 확인해주세요'
    #GET Method    
    return render(request, 'accounts/sign_up.html', context)

def login(request):
    context ={}
    
    #POST Method
    
    if request.method == 'POST':
        if request.POST['email'] and request.POST['password']:
            
            user = auth.authenticate(
                request,
                email=request.POST['email'],
                password=request.POST['password']
            )
            
            if user is not None:
                auth.login(request, user)
                return redirect('posts:index')
            else:
                context['error'] = '아이디와 비밀번호를 다시 확인해주세요.'
            
        else:
            context['error'] = '아이디와 비밀번호를 모두 입력해주세요.'
            
    # GET Method
    return render(request, 'accounts/login.html', context)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('posts:index')