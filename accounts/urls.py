# django imports
from django.urls import path, include
# 3rd party imports
from rest_framework import routers
from accounts.views import (AccountCreationViewset,villages)
from rest_framework_simplejwt.views import (TokenObtainPairView)


route = routers.DefaultRouter()
route.register('account', AccountCreationViewset)

urlpatterns = [
    path('', include(route.urls)),
    path('villages/',villages),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]