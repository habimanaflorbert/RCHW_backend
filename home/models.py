import uuid
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from accounts.models import User,Village

# Create your models here.

class Patient(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    full_name=models.CharField(max_length=255)
    insurance_name=models.CharField(max_length=50)
    insurance_number=models.CharField(max_length=200)
    sickness=models.CharField(max_length=250)
    phone=models.CharField(max_length=13)
    village=models.ForeignKey(Village,related_name='patient_village',on_delete=models.CASCADE)
    date_of_birth=models.DateField(auto_created=False)
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
    phone_number=models.CharField(max_length=10)
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
        ordering = ('family',)

    def __str__(self):
            return self.family

    def get_absolute_url(self):
        return reverse("contraception_detail", kwargs={"pk": self.pk})