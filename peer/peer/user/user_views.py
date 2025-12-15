from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib import messages
from peer.models import CustomUser, Skill, Profile, Review,Listing, Board
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
    # Check if profile already exists
    if Profile.objects.filter(user=request.user).exists():
        return redirect(reverse('user:view_profile', kwargs={'uid': request.user.id}))
    
    if request.method == "POST":
        user = CustomUser.objects.get(username=request.user.username)
        user.last_name = request.POST.get('lname')
        user.first_name = request.POST.get('fname')
        user.save()
        
        state = request.POST.get('state')
        town = request.POST.get('town')
        zipcode = request.POST.get('zip')
        about = request.POST.get('about_me', '')
        
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
        profile.about = request.POST.get('about', '')
        
        user.skills.clear()
        skills_ids = request.POST.getlist("skills")
        for id in skills_ids:
            if id != "":
                # Handle comma-separated values
                for skill_id in id.split(','):
                    skill_id = skill_id.strip()
                    if skill_id:
                        user.skills.add(int(skill_id))
        user.save()
        profile.save()
        return redirect('user:view_profile', uid=user.id)
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
        return redirect('peer:home')
    user = get_object_or_404(CustomUser, pk=uid)
    
    # Get or create profile - this will save to DB if it doesn't exist
    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={
            'town': '',
            'state': '',
            'zipcode': '',
            'about': '',
            'skills': ''
        }
    )
    
    reviews = list(Review.objects.filter(receiver=user))
    listings = list(Listing.objects.filter(author=user).order_by("-created_at"))
    boards = []
    for b in Board.objects.all().order_by("-created"):
        if b.creator == user or b.moderators.filter(id=user.id).exists():
            boards.append(b)
    for m in user.bmessages.all():
        if m.board not in boards:
            boards.append(m.board)
    context = {
        'u' : user,
        'p' : profile,
        'reviews': reviews[:50],
        'listings': listings[:50],
        'boards': boards[:50]
    }
    return render(request, 'display_profile.html', context)

@login_required
def leaveReview(request, uid):
    receiver = get_object_or_404(CustomUser, pk=uid)
    sender = get_object_or_404(CustomUser, pk=request.user.id)
    context = {'u' : receiver}
    review_obj = Review.objects.filter(receiver=receiver, author=sender)[0]
    if review_obj:
        context['rating'] = review_obj.rating
        context['review'] = review_obj.message
    if request.method == "POST":
        rating = request.POST.get("rating")
        review = request.POST.get("review")
        
        if review_obj:
            review_obj.rating = rating
            review_obj.review = review
            review_obj.save()
        else:
            Review.objects.create(author=sender, receiver=receiver, message=review, rating=rating)
        
        num_rev = receiver.rating_count
        total = 0
        for r in receiver.reviews_received.all():
            total += r.rating
        receiver.rating_count += 1 
        receiver.rating = round((total/receiver.rating_count), 3)
        receiver.save()
        return redirect('peer:home')
    
    return render(request, 'create_review.html', context=context)