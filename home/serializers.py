from rest_framework import serializers
from accounts.serializers import UserSerializer,VillageSerializer
from home.models import Patient,HouseHold, Malnutrition,Contraception


class PatientSerializer(serializers.ModelSerializer):
    worker_detail=UserSerializer(source='worker',read_only=True)
    village_detail=VillageSerializer(source='village',read_only=True)
    worker = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model=Patient
        fields=(
            'id',
            'full_name',
            'insurance_name',
            'insurance_number',
            'sickness',
            'phone',
            'village_detail',
            'date_of_birth',
            'worker',
            'worker_detail',
            'created_on'
        )
    

class HouseHoldSerializer(serializers.ModelSerializer):
    worker_detail=UserSerializer(source='worker',read_only=True)
    village_detail=VillageSerializer(source='village',read_only=True)
    worker = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model=HouseHold
        fields=(
            'id',
            'father_full_name',
            'father_id_no',
            'mother_full_name',
            'mother_id_no',
            'number_child',
            'phone_number',
            'worker',
            'worker_detail',
            'village_detail',
            'village',
            'created_on'
        )

class MalnutritionSerializer(serializers.ModelSerializer):
    family_detail=HouseHoldSerializer(source='family',read_only=True)
    worker = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model= Malnutrition
        fields=(
            'id',
            'family',
            'family_detail',
            'child_full_name',
            'has_malnutrition',
            'worker',
            'created_on'
        )


class ContraceptionSerializer(serializers.ModelSerializer):
    family_detail=HouseHoldSerializer(source='family',read_only=True)
    worker = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model=Contraception
        fields=(
            'id',
            'family',
            'family_detail',
            'description',
            'worker',
            'created_on'
        )


 