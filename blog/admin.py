from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, BlogPost, Like, Comment, OTP

admin.site.register(BlogPost)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(OTP)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass
