from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib import messages
from peer.models import CustomUser, Skill, Profile, Review
from django.urls import reverse

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

@login_required
def createProfile(request):
    if request.method == "POST":
        user = CustomUser.objects.get(username=request.user.username)
        user.last_name = request.POST.get('lname')
        user.first_name = request.POST.get('fname')
        user.save()
        
        state = request.POST.get('state')
        town = request.POST.get('town')
        zipcode = request.POST.get('zip')
        about = request.POST.get('about_me')
        
        Profile.objects.create(user=user, town=town, state=state, zipcode=zipcode, about=about)
        return redirect(reverse('user:view_profile', kwargs={'uid': user.id})) 
    return render(request, 'create_profile.html', {'action':'create'})

@login_required
def updateProfile(request):
    user = CustomUser.objects.get(username=request.user.username)
    profile = get_object_or_404(Profile, user=user)
    if request.method == "POST":
        user.last_name = request.POST.get('lname')
        user.first_name = request.POST.get('fname')
        
        profile.state = request.POST.get('state')
        profile.town = request.POST.get('town')
        profile.zipcode = request.POST.get('zip')
        
        user.skills.clear()
        skills_ids = request.POST.getlist("skills")
        for id in skills_ids:
            if id != "":
                user.skills.add(int(id))
        user.save()
        profile.save()
        return redirect(reverse('user:view_profile', kwargs={'uid': user.id}))
    context ={
        'finame' : user.first_name,
        'laname' : user.last_name,
        'ustate' : profile.state,
        'utown' : profile.town,
        'uzip' : profile.zipcode,
        'uabout': profile.about,
        'user_skills': user.skills.all(),
        'skills' : Skill.objects.all(),
        'action' : 'update'
    }
    return render(request, 'create_profile.html', context)

@login_required
def viewProfile(request, uid):
    if not Profile.objects.filter(user=request.user).exists():
        if request.user.id == uid:
            return redirect('user:create_profile')
        return redirect('peer:home') #Possibly Replace with a standard 404-esq 
    user = get_object_or_404(CustomUser, pk=uid)
    profile = get_object_or_404(Profile, user=user)
    reviews = list(Review.objects.filter(receiver=user))
    context = {
        'u' : user,
        'p' : profile,
        'reviews': reviews[:5]
    }
    return render(request, 'display_profile.html', context)

@login_required
def leaveReview(request, uid):
    receiver = get_object_or_404(CustomUser, pk=uid)
    sender = get_object_or_404(CustomUser, pk=request.user.id)
    if request.method == "POST":
        rating = request.POST.get("rating")
        review = request.POST.get("review")
        
        Review.objects.create(author=sender, receiver=receiver, message=review, rating=rating)
        
        num_rev = receiver.rating_count
        cur_rat = receiver.rating
        receiver.rating = round((((cur_rat*num_rev)+rating) / (num_rev+1)), 3) #decide wether it's worth it to recalculate the true mean using Review object 
        receiver.rating_count += 1 
        receiver.save()
        redirect('peer:home')
    #add logic to prevent more than one review on the same person
    return render(request, 'create_review.html', {'u' : receiver})