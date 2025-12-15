from django.contrib import admin
from .models import *


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_request', 'price', 'created_at')
    list_filter = ('is_request',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'sender', 'recipient', 'listing', 'created_at')
    search_fields = ('sender_name', 'content')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_login', 'email', 'username', 'rating', 'rating_count', 'date_joined')
    search_fields = ('username', 'email', 'rating')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'skill', 'description', 'title', 'created', 'creator')
    search_fields = ('id', 'skill', 'creator')

@admin.register(BoardMessage)
class BoardMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'poster', 'content', 'reply_to', 'board', 'depth', 'time_posted')
    search_fields = ('id', 'poster', 'board')