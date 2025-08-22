from django.contrib import admin
from .models import Querry, Signup,Answers,Rating

class SignupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'Year', 'Branch', 'date']  # Adjusted list_display



class QuerryAdmin(admin.ModelAdmin):
    list_display = ['query_id','user', 'name', 'email', 'desc', 'date', 'Cat']

admin.site.register(Signup, SignupAdmin)
admin.site.register(Querry,QuerryAdmin)
admin.site.register(Answers)
admin.site.register(Rating)