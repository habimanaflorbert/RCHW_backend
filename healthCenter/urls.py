from django.urls import path
from healthCenter.views import (assign_pregnancy,assign_kid,change_location, remove_birth, remove_pregnancy,user_logout,change_pass,active_user,disactive_user,settings_user,delete_birth,edit_birth,delete_pregnancy,edit_pregnancy,pregnancy_woman,birth_child,house_hold,patient,login,home_health_center,malnutrition,contraception,members)

urlpatterns = [
    path('',login,name='login'),
    path('home/',home_health_center,name='home_health_center'),
    path('malnutrition/',malnutrition,name="malnutrition"),
    path('contraception/',contraception,name="contraception"),
    path('members/',members,name="members"),
    path('patient/',patient,name="patient"),
    path('family/',house_hold,name="house_hold"),
    path('birth-kid/',birth_child,name="birth_child"),
    path('pregnancy-women/',pregnancy_woman,name="pregnancy_woman"),
    path('edit-pregnancy/<uuid:pk>/',edit_pregnancy,name="edit_pregnancy"),
    path('edit-child/<uuid:pk>/',edit_birth,name="edit_birth"),
    path('delete-pregnancy/<uuid:pk>/',delete_pregnancy,name="delete_pregnancy"),
    path('delete-birth/<uuid:pk>/',delete_birth,name="delete_birth"),
    path('setting/',settings_user,name="settings_user"),
    path('disactive/<uuid:pk>/',disactive_user,name="disactive_user"),
    path('active/<uuid:pk>/',active_user,name="active_user"),
    path('change/pass/',change_pass,name="change_pass"),
    path('logout/',user_logout,name="logout"),
    path('change/location/',change_location,name="change_location"),
    path('assign/kid/<uuid:pk>/',assign_kid,name="assign_kid"),
    path('assign/pregnancy/<uuid:pk>/',assign_pregnancy,name="assign_pregnancy"),
    path('remove/pregnancy/<uuid:pk>/',remove_pregnancy,name="remove_pregnancy"),
    path('remove/birth/<uuid:pk>/',remove_birth,name="remove_birth"),
    

]