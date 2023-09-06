import uuid
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from home.models import HouseHold
from accounts.models import User,Village

# Create your models here.

class BirthChild(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    full_name=models.CharField(max_length=255)
    family=models.ForeignKey(HouseHold,related_name='child_family',on_delete=models.CASCADE)
    description= models.TextField(blank=True)
    clinic=models.ForeignKey(User,related_name='child_clinic',on_delete=models.CASCADE)
    village=models.ForeignKey(Village,related_name='child_village',on_delete=models.CASCADE)
    birth_date=models.DateTimeField(auto_now_add=False)
    vigirant=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='vigitant_birth',blank=True, null=True)
    is_valid= models.BooleanField(_("active"), default=True)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)

    class Meta:
        verbose_name = _("Birth Child")
        verbose_name_plural = _("Birth Children")
        ordering = ('created_on',)

    def __str__(self):
            return self.full_name

    def get_absolute_url(self):
        return reverse("birth_child_detail", kwargs={"pk": self.pk})

class Pregnancy(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    full_name=models.CharField(max_length=255)
    description= models.TextField(blank=True)
    phone=models.CharField(max_length=13)
    birth_date=models.DateTimeField(auto_now_add=False)
    village=models.ForeignKey(Village,related_name='pregant_village',on_delete=models.CASCADE)
    give_birth=models.BooleanField(default=False)
    clinic=models.ForeignKey(User,related_name='pregnancy_clinic',on_delete=models.CASCADE)
    vigirant=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='vigitant_pregnancy',blank=True, null=True)
    is_valid= models.BooleanField(_("active"), default=True)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)

    class Meta:
        verbose_name = _("Pregnancy")
        verbose_name_plural = _("Pregnancies")
        ordering = ('created_on',)

    def __str__(self):
            return self.full_name

    def get_absolute_url(self):
        return reverse("pregnancy_detail", kwargs={"pk": self.pk})

