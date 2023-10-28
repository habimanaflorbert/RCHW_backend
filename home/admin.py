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
  
@admin.register(Documenation)
class DocumenationAdmin(admin.ModelAdmin):
    list_display = ('document_name','user_related','is_verify','user','created_on')
    list_display_links = ['document_name']
    search_fields = ['document_name']
    list_filter = ("user_related",)
    actions = [
        "accept_document",
        "reject_document",
    ]
    fields = ('document_name', 'user_related', 'document_file',)
    
    def accept_document(self, request, queryset):
        queryset.update(is_verify=True)
        
    def reject_document(self, request, queryset):
        queryset.update(is_verify=False)
  
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.is_verify=True
        return super().save_model(request, obj, form, change)



@admin.register(BookingMedical)
class BookingMedicalAdmin(admin.ModelAdmin):
    list_display = ('full_name','phone_number','created_on')
    list_display_links = ['full_name']
    search_fields = ['full_name','phone_number']
    list_filter = ("created_on",)
