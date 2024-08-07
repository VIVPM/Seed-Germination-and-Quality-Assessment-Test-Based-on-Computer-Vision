from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class UserModel(UserAdmin):
    list_display = ['username','user_type']

admin.site.register(CustomUser, UserModel)

admin.site.register(Grower)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Crop)
admin.site.register(Variety)
admin.site.register(Season)
admin.site.register(Agency)
admin.site.register(Field_worker)
admin.site.register(Branch)
admin.site.register(Contact)
admin.site.register(Profile)