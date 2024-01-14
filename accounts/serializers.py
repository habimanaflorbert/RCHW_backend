from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from rest_framework import serializers
from accounts.models import Deases, User,Sector,Village,UserAddress,Province,District


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Province
        fields=(
            'id',
            'name'
        )

class DistrictSerializer(serializers.ModelSerializer):
    province_detail=ProvinceSerializer(source='province',read_only=True)
    class Meta:
        model=District
        fields=(
            'id',
            'name',
            'province_detail'
        )

class SectorSerializer(serializers.ModelSerializer):
    district_detail=DistrictSerializer(source='district',read_only=True)
    class Meta:
        model=Sector
        fields=(
            'id',
            'name',
            'district_detail',
        )



class VillageSerializer(serializers.ModelSerializer):
    sector_detail=SectorSerializer(source='sector',read_only=True)
    class Meta:
        model=Village
        fields=(
            'id',
            'name',
            'sector_detail'
        )

class AccountCreationSerializer(serializers.ModelSerializer):
    user_village=serializers.UUIDField(required=True)

    def validate_user_village(self,village):
        try:
            village_inst=Village.objects.get(id=village)
            return village_inst
        except Village.DoesNotExist:
            return serializers.ValidationError("Village doesn't exist")


    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'full_name',
            'phone_number',
            'identification_number',
            'password',
            'user_village'
        )
        extra_kwargs = {"password": {"write_only": True},"user_village": {"write_only": True}}
    def create(self, validated_data):
        village_instance=self.validated_data.pop('user_village',None)
        user = User.objects.create_user(
            full_name=validated_data.get('full_name'), email=validated_data.get('email'), phone_number=validated_data.get('phone_number'), username=validated_data.get('phone_number'), password=validated_data.get('password'))
        address_inst,_=UserAddress.objects.get_or_create(user=user,village=village_instance)

        
        return user

class UserSerializer(serializers.ModelSerializer):
 
    class Meta:
        model=User
        fields=(
            'id',
            'full_name',
            'email',
            'username',
            'phone_number',
            'identification_number',
            'user_type',
            'user_village_name',
            'malnutrition_village',
            'family_village',
            'patient_month',
            'contraception_month'
        )


class UserPasswordSerializer(serializers.ModelSerializer):
    recent_password=serializers.CharField(required=True)
    new_password=serializers.CharField(required=True)
    user= serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self,data):
        if check_password(data.get('recent_password'), data.get('user').password):
            if data.get('new_password') != data['recent_password']:
                return data
            raise  serializers.ValidationError("Password don't match")
        raise serializers.ValidationError("Use Correct password")
    
    class Meta:
        model=User
        fields=(
            'id',
            'recent_password',
            'new_password',
            'user'
        )
    

class DeasesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Deases
        fields=(
            'id',
            'name'
        )
