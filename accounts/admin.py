from django.contrib import admin
from accounts.forms import UserAdminCreationForm, UserAdminChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth import get_user_model
from accounts.models import ClinicAddress, Deases,User,UserAddress,Province,District,Sector,Village,ClinicWorker
from accounts.forms import send_mail_task,get_random_string

class ClinicAddressTabularInline(admin.StackedInline):
    model = ClinicAddress
    # readonly_fields = ['sector']
    extra = 0

class UserAdmin(BaseUserAdmin, admin.ModelAdmin,):
    # The forms to add and change user instances
    inlines=[ClinicAddressTabularInline]
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    list_display = (
        "username",
        "full_name",
        "email",
        "user_type",
        "is_active",
        "phone_number",
        "identification_number",
       
    )
    list_filter = (
        "user_type",
        "is_active",

    )
    fieldsets = (
        (None, {"fields": (
            "username",
            "email",
            "password",
       
        )}),
        (
            "Personal info",
            {
                "fields": (
                    "full_name",
                    "phone_number",
                    "identification_number",
                    "user_type",
                )
            },
        ),
        (
        "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    'groups', 
                    'user_permissions',

                )
            },
        ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": (
            "email",
            "full_name",
            "username",
            "user_type",
            "phone_number",
         
        )}),
    )
    search_fields = (
        "email",
        "username",
        "full_name",
        "phone_number",
    )

    ordering = ("full_name",)
    filter_horizontal = ()
    actions = [
        "disable_users",
        "enable_users",
    ]
    
    
    def save_model(self, request, obj, form, change):
        if change:
            pass
        else:
            password=get_random_string(8)
            obj.set_password(password)
            obj.save()
            message=f"Hello {form.data['full_name'] }! \n You have granted permission web app of RHW as health center of {request.user.full_name} here's crendetials:\n username:{form.data['username']} \n password:{password} \nPlease change password after login to the system \nThank you for using RHW.  "
            subj="You have granted to be permission"
            send_mail_task(message,subj,form.data['email'])
            # send_mail_task(obj.id,form.data['password1'])
        return super().save_model(request, obj, form, change)


    def disable_users(self, request, queryset):
        queryset.update(is_active=False)

    def enable_users(self, request, queryset):
        queryset.update(is_active=True)



    def has_add_permission(self, request) -> bool:
        if request.user.is_staff :
            return True
        return False

admin.site.register(User, UserAdmin)





class DistrictTabularInline(admin.StackedInline):
    model = District
    extra = 1


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    inlines=[DistrictTabularInline]
    list_display = ('name',)
    search_fields = ['name',]
    
    
class VillageTabularInline(admin.StackedInline):
    model = Village
    extra = 1

    
@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    inlines=[VillageTabularInline]
    list_display = ('name',)
    search_fields = ['name',]
    
@admin.register(ClinicWorker)
class ClinicWorkerAdmin(admin.ModelAdmin):
    list_display = ('clinic',)
    search_fields = ['clinic',]
    
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['members'].queryset = User.objects.filter(user_type=User.UMUJYANAMA)
        return super().render_change_form(request, context, *args, **kwargs)


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'village')
    list_display_links = ['user']
    search_fields = ['user']
    
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['user'].queryset = User.objects.filter(user_type=User.UMUJYANAMA)
        return super().render_change_form(request, context, *args, **kwargs)

    

    


@admin.register(ClinicAddress)
class ClinicAddressAdmin(admin.ModelAdmin):
    list_display = ('clinic', 'sector')
    list_display_links = ['clinic']
    search_fields = ['clinic']
    
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['clinic'].queryset = User.objects.filter(user_type=User.HC)
        return super().render_change_form(request, context, *args, **kwargs)

@admin.register(Deases)
class DeasesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ['name']
    search_fields = ['name']
    



admin.site.index_template='admin/admin_user.html'
admin.site.site_header = "RHW"
admin.site.site_title = "RHW"
admin.site.index_title = ""