from datetime import datetime
from django.db import models

# Create your models here.
import uuid

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext as _
from django.urls import reverse

# Create your models here.

class UserManager(BaseUserManager):
 
    def create_user(self, username, full_name, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
    
        user = self.model(           
            username=username,
            full_name=full_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, username, full_name, password=None, **extra_fields
    ):
        """
        Creates and saves a admin with the given email and password.
        """
        user = self.create_user(
            email=email,
            username=username,
            full_name=full_name,
            user_type=User.ADMIN,
            password=password,
            **extra_fields,
        )
        
        user.is_active = True
        user.is_staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    ADMIN="ADMIN"
    UMUJYANAMA="UMUJYANAMA"
    HC="HC"
    STAFF="STAFF"
    RSSB="RSSB"
    RAMA="RAMA"


    USER_TYPE_CHOICE = (
        (ADMIN,"Super User"),
        (STAFF,"Staff User"),
        (UMUJYANAMA,"Umujyana"),
        (HC,"Health Center"),
       
    )

   
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField("email address", max_length=255, unique=True,blank=True,null=True)
    full_name = models.CharField(_("full name"), max_length=100)
    username = models.CharField(_("username"), max_length=100, unique=True)
    # unique phone number as it is a medium for user recognition
    phone_number = models.CharField(
        _("phone number"), max_length=255,unique=True
    )
    identification_number= models.CharField(_("identification_number"),max_length=16)
    user_type = models.CharField(
        _("user type"), choices=USER_TYPE_CHOICE, max_length=50, default=UMUJYANAMA
    )
    is_active = models.BooleanField(_("is active"), default=True)
    # a admin user; non super-user
    is_staff = models.BooleanField(_("staff"), default=False)
    is_first_login = models.BooleanField(_("staff"), default=True)

    admin = models.BooleanField(_("admin"), default=False)  # a admin
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    objects = UserManager()
    USERNAME_FIELD = _("username")
    REQUIRED_FIELDS = ["email","full_name"]

    def get_full_name(self):
        # The user is identified by their address
        return self.full_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.full_name

    def __str__(self):  # __unicode__ on Python 2O
        return self.full_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def user_village(self):
        try:
            return self.user_address.village.id
        except:
            return None
    
    @property
    def user_village_name(self):
        try:
            return self.user_address.village.name
        except:
            return None

    @property
    def malnutrition_village(self):
        return self.umujyanama_malnutrition.all().count()

    @property
    def family_village(self):
        return self.umujyanama_family.all().count()

    @property
    def patient_month(self):

        return self.umujyanama_patient.all().count()

    @property
    def contraception_month(self):
        return self.umujyanama_contraception.all().count()
    @property
    def clinic_members(self):
        return self.clinic.members.all()

class Province(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name=models.CharField(max_length=50)


    class Meta:
        verbose_name = _("Province")
        verbose_name_plural = _("Provinces")
        ordering = ('name',)

    def __str__(self):
            return self.name

    def get_absolute_url(self):
        return reverse("province_detail", kwargs={"pk": self.pk})


class District(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name=models.CharField(max_length=50)
    province=models.ForeignKey(Province,on_delete=models.CASCADE,related_name='province')


    class Meta:
        verbose_name = _("District")
        verbose_name_plural = _("Districts")
        ordering = ('name',)

    def __str__(self):
            return self.name

    def get_absolute_url(self):
        return reverse("district_detail", kwargs={"pk": self.pk})



class Sector(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name=models.CharField(max_length=50)
    district=models.ForeignKey(District,on_delete=models.CASCADE,related_name='province_sector')


    class Meta:
        verbose_name = _("Sector")
        verbose_name_plural = _("Sectors")
        ordering = ('name',)

    def __str__(self):
            return self.name

    def get_absolute_url(self):
        return reverse("sector_detail", kwargs={"pk": self.pk})


class Village(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name=models.CharField(max_length=50)
    sector=models.ForeignKey(Sector,on_delete=models.CASCADE,related_name='village')


    class Meta:
        verbose_name = _("Village")
        verbose_name_plural = _("Villages")
        ordering = ('name',)

    def __str__(self):
            return self.name

    def get_absolute_url(self):
        return reverse("village_detail", kwargs={"pk": self.pk})



class UserAddress(models.Model):
    user=models.OneToOneField(User,related_name='user_address',on_delete=models.CASCADE)
    village=models.ForeignKey(Village,on_delete=models.CASCADE,related_name='user_village')

    class Meta:
        verbose_name = _("User Address")
        verbose_name_plural = _("User addresses")
        ordering = ('village',)


    def get_absolute_url(self):
        return reverse("user_address_detail", kwargs={"pk": self.pk})


class ClinicWorker(models.Model):
    clinic=models.OneToOneField(User,related_name='clinic',on_delete=models.CASCADE)
    members=models.ManyToManyField(User,related_name='members')

    class Meta:
        verbose_name = _("Clinic Worker")
        verbose_name_plural = _("Clinic Workers")
        ordering = ('clinic',)


    def get_absolute_url(self):
        return reverse("clinic_detail", kwargs={"pk": self.pk})
    

class ClinicAddress(models.Model):
    clinic=models.OneToOneField(User,related_name='clinic_address',on_delete=models.CASCADE)
    sector=models.ForeignKey(Sector,on_delete=models.SET_NULL,related_name='clinic_sector',blank=True, null=True)

    class Meta:
        verbose_name = _("Clinic address")
        verbose_name_plural = _("Clinics address")
        ordering = ('sector',)


    def get_absolute_url(self):
        return reverse("clinic_address_detail", kwargs={"pk": self.pk})


class Deases(models.Model):
    name=models.CharField(max_length=50)


    class Meta:
        verbose_name = _("dease")
        verbose_name_plural = _("deases")
        ordering = ('name',)

    def __str__(self):
            return self.name

    def get_absolute_url(self):
        return reverse("province_detail", kwargs={"pk": self.pk})
