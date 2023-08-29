import datetime
from rest_framework.viewsets import mixins
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,BasePermission
from rest_framework.decorators import action


from home.models import Documenation, Patient,HouseHold,Malnutrition,Contraception
from home.serializers import DocumenationSerializer, PatientSerializer,HouseHoldSerializer,MalnutritionSerializer,ContraceptionSerializer

# Create your views here.

class PatientViewset(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [BasePermission]
    queryset = Patient.objects.all()


    def get_queryset(self):
        return Patient.objects.filter(worker=self.request.user)

    @action(['GET'],detail=False)
    def details(self,request):
        try:
            id=request.GET.get('id')
            query=Patient.objects.get(id=id)
            serializer = self.get_serializer(query)
           
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({},status=status.HTTP_200_OK)
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(village=request.user.user_address.village)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):

        instance=self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

    @action(['DELETE'],detail=False)
    def delete(self,request):
        ob=Patient.objects.filter(id=self.GET.get('id'),worker=self.request.user)
        if ob.exists():
            ob.delete()
            return Response({"msg":"has deleted"})
        return Response({"msg":"no data found"})



class HouseHoldViewset(viewsets.ModelViewSet):
    serializer_class = HouseHoldSerializer
    permission_classes = [BasePermission]
    queryset = HouseHold.objects.all()


    def get_queryset(self):
        return HouseHold.objects.filter(village__id=self.request.user.user_village)

    @action(['GET'],detail=False)
    def details(self,request):
        try:
            id=request.GET.get('id')
            query=HouseHold.objects.get(id=id)
            serializer = self.get_serializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except HouseHold.DoesNotExist:
            return Response({},status=status.HTTP_200_OK)
        

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(['DELETE'],detail=False)
    def delete(self,request):
        ob=HouseHold.objects.filter(id=self.request.GET.get('id'),worker=self.request.user)
        if ob.exists():
            ob.delete()
            return Response({"msg":"has deleted"})
        return Response({"msg":"no data found"})




class MalnutritionViewset(viewsets.ModelViewSet):
    serializer_class = MalnutritionSerializer
    permission_classes = [BasePermission]
    queryset = Malnutrition.objects.all()


    def get_queryset(self):
        return Malnutrition.objects.filter(family__village=self.request.user.user_village)

    @action(['GET'],detail=False)
    def details(self,request):

        try:
            id=request.GET.get('id')
            query=Malnutrition.objects.get(id=id)
            serializer = self.get_serializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Malnutrition.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        instance =self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(['DELETE'],detail=False)
    def delete(self,request):
        ob=Malnutrition.objects.filter(id=self.GET.get('id'),worker=self.request.user)
        if ob.exists():
            ob.delete()
            return Response({"msg":"has deleted"})
        return Response({"msg":"no data found"})



class ContraceptionViewset(viewsets.ModelViewSet):
    serializer_class = ContraceptionSerializer
    permission_classes = [BasePermission]
    queryset = Contraception.objects.all()

    def get_queryset(self): 
        return Contraception.objects.filter(worker=self.request.user)

    @action(['GET'],detail=False)
    def details(self,request):
        try:
            id=request.GET.get('id')
            query=Contraception.objects.get(id=id,worker=self.request.user)
            serializer = self.get_serializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Contraception.DoesNotExist:
            return Response({},status=status.HTTP_200_OK)
        

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def patch(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
    
    @action(['DELETE'],detail=False)
    def delete(self,request):
        ob=Contraception.objects.filter(id=request.GET.get('id'),worker=self.request.user)
        if ob.exists():
            ob.delete()
            return Response({"msg":"has deleted"})
        return Response({"msg":"no data found"})


class DocumentationViewset(viewsets.ModelViewSet):
    serializer_class = DocumenationSerializer
    permission_classes = [BasePermission]
    queryset = Documenation.objects.all()


    def get_queryset(self):
        return Documenation.objects.filter(user_related=self.request.user.user_type,is_verify=True)

    @action(['GET'],detail=False)
    def detail(self,request):
        try:
            id=request.GET.get('id')
            query=Documenation.objects.get(id=id,is_verify=True)
            serializer = self.get_serializer(query)
           
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Documenation.DoesNotExist:
            return Response({},status=status.HTTP_204_NO_CONTENT)
    