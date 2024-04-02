from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


@login_required(login_url ='login' )
def recepie(request):
    if request.method == "POST":
        data = request.POST
        recepie_image = request.FILES.get('recepie_image')
        recepie_name = data.get('recepie_name')
        recepie_description = data.get('recepie_description')
        
        Recepie.objects.create(
             recepie_image = recepie_image,
             recepie_name =  recepie_name,
             recepie_description =recepie_description
             )
        return redirect('/recepie/')
    queryset=Recepie.objects.all()
    
    if request.GET.get('search'):
       queryset=queryset.filter(recepie_name__icontains = request.GET.get('search'))
       
    context ={
        'recepies': queryset
    }
        
    return render(request,'recepie.html',context)

def update_recepie(request,id):
     queryset=Recepie.objects.get(id=id)
     if request.method == "POST":
            data = request.POST
            recepie_image = request.FILES.get('recepie_image')
            recepie_name = data.get('recepie_name')
            recepie_description = data.get('recepie_description')
            
            queryset.recepie_name =recepie_name 
            queryset.recepie_description =recepie_description
            if recepie_image:
                queryset.recepie_image =recepie_image
            queryset.save()
            return redirect('/recepie/')
   
     context ={
         'recepie': queryset
     }   
     return render(request,'update_recepie.html',context)

def delete_recepie(request,id):
    queryset =Recepie.objects.get(id = id)
    queryset.delete()
    return redirect('/logout/')


def login_page(request):
    if request.method == "POST":
        
        username=request.POST.get('username')
        password=request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            messages.error(request,'invalid username')
            return redirect('login')
        user=authenticate(username=username,password=password)
        
        if user is None:
            messages.error(request,'invalid name')
            return redirect('login')
        else:
            login( request,user)
            return redirect('/recepie/')
    return render(request,'login.html')


def logout_page(request):
    logout(request)
    return redirect('login')


def register_page(request):
    if request.method =="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user=User.objects.filter(username=username)
        if user.exists():
            messages.error(request, 'username is already exist')
            return redirect('/register/')
        
        user=User.objects.create(first_name=first_name,last_name=last_name,username=username)
        user.set_password(password)
        user.save()
        messages.success(request,'Account created succesfully')
        return redirect('login')
        

    return render(request,'register.html')