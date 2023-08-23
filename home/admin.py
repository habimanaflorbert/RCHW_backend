from django.contrib import admin
from home.models import *
# Register your models here.


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'sickness','worker','created_on')
    list_display_links = ['full_name']
    search_fields = ['sickness','full_name']
   

@admin.register(HouseHold)
class HouseHoldAdmin(admin.ModelAdmin):
    list_display = ('father_full_name', 'mother_full_name','number_child','village')
    list_display_links = ['father_full_name']
    search_fields = ['father_full_name','mother_full_name','village']

@admin.register(Malnutrition)
class MalnutritionAdmin(admin.ModelAdmin):
    list_display = ('family', 'child_full_name','has_malnutrition')
    list_display_links = ['family']
    search_fields = ['child_full_name','family']
   



@admin.register(Contraception)
class ContraceptionAdmin(admin.ModelAdmin):
    list_display = ('family','created_on')
    list_display_links = ['family']
    search_fields = ['family']
  
