# django imports
from django.urls import path, include
# 3rd party imports
from rest_framework import routers
from home.views import (BookingViewset,PregnancyViewset,ChildViewset,DocumentationViewset,PatientViewset,HouseHoldViewset,MalnutritionViewset,ContraceptionViewset)


route = routers.DefaultRouter()
route.register('patient', PatientViewset)
route.register('family',HouseHoldViewset)
route.register('malnutrition',MalnutritionViewset)
route.register('contraception',ContraceptionViewset)
route.register('document',DocumentationViewset)
route.register('child/born',ChildViewset)
route.register('pregnancy',PregnancyViewset)
route.register('booking',BookingViewset)

urlpatterns = [
    path('', include(route.urls)),
]