from django.contrib import admin

from .models import (User, Review, Comment,
                     Title, Category, Genre)

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
