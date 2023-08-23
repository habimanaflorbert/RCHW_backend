from django.urls import path, include
from healthCenter.views import (house_hold,patient,login,home_health_center,malnutrition,contraception,members)

urlpatterns = [
    path('',login,name='login'),
    path('home/',home_health_center,name='home_health_center'),
    path('malnutrition/',malnutrition,name="malnutrition"),
    path('contraception/',contraception,name="contraception"),
    path('members/',members,name="members"),
    path('patient/',patient,name="patient"),
    path('family/',house_hold,name="house_hold"),
]