from django.contrib import admin
from accounts.forms import UserAdminCreationForm, UserAdminChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth import get_user_model
from accounts.models import ClinicAddress,User,UserAddress,Province,District,Sector,Village,ClinicWorker
from accounts.forms import send_mail_task,get_random_string

class UserAdmin(BaseUserAdmin, admin.ModelAdmin,):
    # The forms to add and change user instances
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
            "password1",
            "password2"
          
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
            message=f"Hello {form.data['full_name'] }! \n You have granted permission web app of RCHW as health center of {request.user.full_name} here's crendetials:\n username:{form.data['username']} \n password:{form.data['password1']} \nPlease change password after login to the system \nThank you for using RCHW.  "
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

admin.site.register(Province)
admin.site.register(District)
admin.site.register(Sector)
admin.site.register(Village)
admin.site.register(ClinicWorker)

@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'village')
    list_display_links = ['user']
    search_fields = ['user']

@admin.register(ClinicAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('clinic', 'sector')
    list_display_links = ['clinic']
    search_fields = ['clinic']


admin.site.index_template='admin/admin_user.html'
admin.site.site_header = "RCHW"
admin.site.site_title = "RCHW"
admin.site.index_title = ""