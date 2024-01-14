# django imports
from django.urls import path, include
# 3rd party imports
from rest_framework import routers
from accounts.views import (AccountCreationViewset, deases,villages)
from rest_framework_simplejwt.views import (TokenObtainPairView)


route = routers.DefaultRouter()
route.register('account', AccountCreationViewset)
# route.register('login', AccountCreationViewset)

urlpatterns = [
    path('', include(route.urls)),
    path('villages/',villages),
    path('deases/',deases),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  
]