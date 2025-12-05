from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib import messages
from peer.models import CustomUser, Skill

def loginPage(request):
    if request.method == 'POST': 
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not CustomUser.objects.filter(email=email).exists():
            messages.error(request, "No account associated with this email")
            return redirect('user:login')
        username = CustomUser.objects.get(email=email).username
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('peer:home')
        else:
            context = {'message' : 'email or password incorrect'}
            return render(request, 'login.html', context)
    return render(request, 'login.html')
            

def registerPage(request):
    skills = Skill.objects.all()
    context = {'skills':skills}
    if request.method == 'POST':
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')
        username = request.POST.get('username')
        emailAddr = request.POST.get('email')
        
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('user:register')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('user:register')
        
        if CustomUser.objects.filter(email=emailAddr).exists():
            messages.error(request, "Email  already in use")
            return redirect('user:register')
        
        n_a = CustomUser.objects.create_user(username, emailAddr, password1)
        skills_ids = request.POST.getlist("skills")
        for id in skills_ids:
            if id != "":
                n_a.skills.add(int(id))
        user = authenticate(request, username=username, password=password1)
        login(request, user)
        return redirect('peer:home')
    
    return render(request, 'register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('user:login')