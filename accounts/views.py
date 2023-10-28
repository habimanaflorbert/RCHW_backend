from rest_framework.viewsets import mixins
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,BasePermission
from rest_framework.decorators import api_view

from accounts.models import User,Village
from accounts.serializers import AccountCreationSerializer,VillageSerializer,UserSerializer,UserPasswordSerializer
from rest_framework.decorators import action
# Create your views here.

class AccountCreationViewset(viewsets.ModelViewSet):
    serializer_class = AccountCreationSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    
    def get_permissions(self):
        if self.request.method == 'PUT':
            self.permission_classes = [BasePermission]
        elif self.request.method =="GET":
            self.permission_classes = [BasePermission]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'user_me':
            return UserSerializer
        elif self.action=='password':
            return UserPasswordSerializer
        return super().get_serializer_class()


    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @action(['GET'],detail=False)
    def user_me(self,request):
        try:

            query= User.objects.get(id=self.request.user.id)
            serializer = self.get_serializer(query)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({})
    
    @action(['PATCH','POST'],detail=False)
    def password(self,request):
        serializer = self.get_serializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.get('user').set_password(serializer.validated_data.get("new_password"))
        serializer.validated_data.get('user').save()
        return Response({"mg":"password changed"}, status=status.HTTP_201_CREATED)



    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"mg":"account created"}, status=status.HTTP_201_CREATED)
    
    def patch(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@api_view(["GET"])
def villages(request):
    villages=Village.objects.all()
    serializer=VillageSerializer(villages,many=True)
    return Response(serializer.data)

