from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Register your models here.


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(MainCourse)
admin.site.register(Curriculam)
admin.site.register(Customer)