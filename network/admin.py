from django.contrib import admin
from .models import User,Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('owner', 'content','created_date','likes')
admin.site.register(Post, PostAdmin)