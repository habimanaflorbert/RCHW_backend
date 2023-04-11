import datetime
from rest_framework.viewsets import mixins
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,BasePermission
from rest_framework.decorators import action


from home.models import Patient,HouseHold,Malnutrition,Contraception
from home.serializers import PatientSerializer,HouseHoldSerializer,MalnutritionSerializer,ContraceptionSerializer

# Create your views here.

class PatientViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = PatientSerializer
    permission_classes = [BasePermission]
    queryset = Patient.objects.all()


    def get_queryset(self):
        return Patient.objects.filter(worker=self.request.user)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(village=request.user.user_address.village)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

class HouseHoldViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = HouseHoldSerializer
    permission_classes = [BasePermission]
    queryset = Patient.objects.all()


    def get_queryset(self):
        print()
        print()
        print(self.request.user.user_village)
        print()

        print()

        return HouseHold.objects.filter(village__id=self.request.user.user_village)


    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class MalnutritionViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = MalnutritionSerializer
    permission_classes = [BasePermission]
    queryset = Malnutrition.objects.all()


    def get_queryset(self):
        return Malnutrition.objects.filter(family__village=self.request.user.user_address)


    def create(self, request, *args, **kwargs):
        print()
        print(request.data)
        print()

        serializer = self.get_serializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class ContraceptionViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ContraceptionSerializer
    permission_classes = [BasePermission]
    queryset = Contraception.objects.all()


    def get_queryset(self):
        return Contraception.objects.filter(worker=self.request.user)


    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)