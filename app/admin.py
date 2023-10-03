from django.contrib import admin

# Register your models here.

from .models import Avatar, ConfirmEmail, Follow, Image, Post, Reaction, Tags

admin.site.register(Avatar)
admin.site.register(ConfirmEmail)
admin.site.register(Follow)
admin.site.register(Image)
admin.site.register(Post)
admin.site.register(Reaction)
admin.site.register(Tags)
