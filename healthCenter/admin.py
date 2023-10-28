from django.contrib import admin

from .models import *

# Register your models here.
@admin.register(Pregnancy)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone','birth_date','give_birth','clinic','created_on')
    list_display_links = ['full_name']
    search_fields = ['clinic','full_name']
   

@admin.register(BirthChild)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'family','birth_date','clinic','created_on')
    list_display_links = ['full_name']
    search_fields = ['clinic','full_name']

