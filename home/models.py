import uuid
from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.utils.translation import gettext as _
from accounts.models import User,Village

# Create your models here.

class Patient(models.Model):
    MALARIA="MALARIA"
    CHILDILLNESS="CHILDILLNESS"
    TUBERCULOSIS="TUBERCULOSIS"


    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    full_name=models.CharField(max_length=255)
    insurance_name=models.CharField(max_length=50)
    insurance_number=models.CharField(max_length=200)
    sickness=models.CharField(max_length=250)
    phone=models.CharField(max_length=13)
    village=models.ForeignKey(Village,related_name='patient_village',on_delete=models.CASCADE)
    date_of_birth=models.DateField(auto_created=False)
    symptoms=models.TextField()
    causes=models.TextField()
    worker=models.ForeignKey(User,related_name='umujyanama_patient',on_delete=models.CASCADE)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)

    class Meta:
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")
        ordering = ('full_name',)

    def __str__(self):
            return self.full_name

    def get_absolute_url(self):
        return reverse("patient_detail", kwargs={"pk": self.pk})


class HouseHold(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    father_full_name=models.CharField(max_length=250)
    father_id_no= models.CharField(_("father_identification_number"),max_length=16)
    mother_full_name=models.CharField(max_length=250)
    mother_id_no= models.CharField(_("mother_identification_number"),max_length=16)
    number_child=models.IntegerField(default=0)
    phone_number=models.CharField(max_length=16)
    worker=models.ForeignKey(User,related_name='umujyanama_family',on_delete=models.CASCADE)
    village=models.ForeignKey(Village,related_name='family_village',on_delete=models.CASCADE)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)

    class Meta:
        verbose_name = _("House Hold")
        verbose_name_plural = _("House Hold")
        ordering = ('father_full_name',)

    def __str__(self):
            return self.father_full_name

    def get_absolute_url(self):
        return reverse("house_hold_detail", kwargs={"pk": self.pk})



class Malnutrition(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    family=models.ForeignKey(HouseHold,related_name='family_malnutrition',on_delete=models.CASCADE)
    child_full_name=models.CharField(max_length=250)
    has_malnutrition=models.BooleanField(default=True)
    worker=models.ForeignKey(User,related_name='umujyanama_malnutrition',on_delete=models.CASCADE)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)

    class Meta:
        verbose_name = _("Child  Malnutrition")
        verbose_name_plural = _("Children  Malnutrition")
        ordering = ('child_full_name',)

    def __str__(self):
            return self.child_full_name

    def get_absolute_url(self):
        return reverse("sector_detail", kwargs={"pk": self.pk})


class Contraception(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    family=models.ForeignKey(HouseHold,related_name='family_contraception',on_delete=models.CASCADE)
    description=models.TextField()
    worker=models.ForeignKey(User,related_name='umujyanama_contraception',on_delete=models.CASCADE)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)

    class Meta:
        verbose_name = _("Contraception")
        verbose_name_plural = _("Contraception")
        ordering = ('-created_on',)



    def get_absolute_url(self):
        return reverse("contraception_detail", kwargs={"pk": self.pk})
    

class Documenation(models.Model):
    UMUJYANAMA="UMUJYANAMA"
    HC="HC"
    USER="USER"
    
    USER_RELATED = (
        (UMUJYANAMA,"Umujyana"),
        (HC,"Health Center"),
        (USER,"User")
       
    )
    def validate_file_extension(value):
        import os
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.pdf']
        if not ext in valid_extensions:
            raise ValidationError(u'we support Pdf only !')
        
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    document_name=models.CharField(max_length=250)
    user_related=models.CharField(
        _("user related"), choices=USER_RELATED, max_length=50, default=UMUJYANAMA
    )
    is_verify= models.BooleanField(_("is verify"), default=False)
    document_file=models.FileField(upload_to="documentations",validators=[validate_file_extension])
    user=models.ForeignKey(User,related_name='uploaded_by',on_delete=models.CASCADE)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Documenation")
        verbose_name_plural = _("Documenation")
        ordering = ('-created_on',)


    def get_absolute_url(self):
        return reverse("documenation_detail", kwargs={"pk": self.pk})
    
class BookingMedical(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=16)
    village=models.ForeignKey(Village,related_name='booking_village',on_delete=models.CASCADE)
    description=models.TextField()
    is_valid= models.BooleanField(_("is valid"), default=True)
    worker=models.ForeignKey(User,related_name='umujyanama_booked',on_delete=models.SET_NULL,blank=True,null=True)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)

    class Meta:
        verbose_name = _("Booking Medical")
        verbose_name_plural = _("Booking Medicals")
        ordering = ('-created_on',)



    def get_absolute_url(self):
        return reverse("bookinr_medical_detail", kwargs={"pk": self.pk})