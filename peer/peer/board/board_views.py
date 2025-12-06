from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib import messages
from peer.models import CustomUser, Board, Skill
from django.urls import reverse
import re 
from django.core.exceptions import PermissionDenied

@login_required
def create_board(request):
    user = get_object_or_404(CustomUser, pk=request.user.id)
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("desc")
        self = request.POST.get("self")
        skill = request.POST.get("skill")
        s = None
        if skill != "":
            s = Skill.objects.get(pk=s)
        board = Board.objects.create(skill=s, title=title, description=description, creator=user)
        mods = request.POST.get("moderators")
        ms = re.split(r'[\s,]+', mods)
        if self == "yes":
            ms.append(request.user.username)
        success_m = []
        fail_m = []
        for m in ms:
            mod  = CustomUser.objects.filter(username=m)
            if mod:
                board.moderators.add(mod)
                success_m.append(m)
            else:
                fail_m.append(m)
        if len(fail_m) > 0:
            for f in fail_m:
                messages.error(f'{f} is not a valid username')
            if self == "yes":
                success_m.remove(request.user.username)
            context={'btitle':title, 'bdesc':description, 'checked': self, 'bskill' : skill, 'bmods' : ", ".join(success_m)}
            return render(request, "create_board.html", context)
        return redirect("peer:home") #REPLACE WITH BOARD VIS WHEN CREATED
    return render(request, "create_board.html", context={'action' : "create"})

@login_required
def edit_board(request, bid):
    board = get_object_or_404(Board, pk=bid)
    if request == "POST":
        title = request.POST.get("title")
        description = request.POST.get("desc")
        self = request.POST.get("self")
        skill = request.POST.get("skill")
        s = None
        if skill != "":
            s = Skill.objects.get(pk=s)
        board = Board.objects.create(skill=s, title=title, description=description, creator=user)
        mods = request.POST.get("moderators")
        ms = re.split(r'[\s,]+', mods)
        if self == "yes":
            ms.append(request.user.username)
        success_m = []
        fail_m = []
        board.moderators.clear()
        for m in ms:
            mod  = CustomUser.objects.filter(username=m)
            if mod:
                board.moderators.add(mod)
                success_m.append(m)
            else:
                fail_m.append(m)
        if len(fail_m) > 0:
            for f in fail_m:
                messages.error(f'{f} is not a valid username')
            if self == "yes":
                success_m.remove(request.user.username)
            context={'btitle':title, 'bdesc':description, 'checked': self, 'bskill' : skill, 'bmods' : ", ".join(success_m)}
            return render(request, "create_board.html", context)
        return redirect('peer:home')
    m = []
    self = None
    for b in board.moderators:
        if b.username == request.user.username:
            self = "yes"
        else:
            m.append(b)
    context={'btitle': board.title, 'bdesc': board.description, 'checked': self, 'bskill' : board.skill, 'bmods' : ", ".join(m)}
    return render(request, "create_board.html", context)

        
            
