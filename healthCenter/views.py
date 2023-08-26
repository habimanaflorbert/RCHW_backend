from datetime import date
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import auth
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q


from utils.pdf_generator import render_to_pdf
from healthCenter.forms import LoginForm
from accounts.decoration import is_health_center
from home.models import Patient,Contraception,Malnutrition,HouseHold
from accounts.models import Village
from healthCenter.forms import HouseHoldForm


# Create your views here.

User=get_user_model()

def login(request):
    form=LoginForm()
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            user_instance = auth.authenticate(username=form.cleaned_data.get(
                'username'), password=form.cleaned_data.get('password'))
            if user_instance is not None:
                if user_instance.user_type == User.HC:
                    auth.login(request, user_instance)
                    return redirect('home_health_center')
            messages.info(request,'Login Failed')
    return render(request, 'auth/login.html',{"form":form})

@is_health_center
def home_health_center(request):
    from django.db.models import Count
    memebrs=request.user.clinic_members
    records=Patient.objects.filter(worker__in=memebrs)
    this_month_maralia=records.filter(sickness=Patient.MALARIA)
    this_month_child=records.filter(sickness=Patient.CHILDILLNESS)
    this_month_tube=records.filter(sickness=Patient.TUBERCULOSIS)
    all_mal=Malnutrition.objects.filter(worker__in=memebrs,has_malnutrition=True).count()
    all_contra=Contraception.objects.filter(worker__in=memebrs,created_on__month=date.today().month).count()

    context={
        'members':memebrs.count(),
        'malnutrition':all_mal,
        'contraception':all_contra,
        'activites':records.values('worker__full_name','worker__phone_number').annotate(c=Count('worker')).order_by('-c')[:5],
        'this_month_child':this_month_child.filter(created_on__month=date.today().month).count(),
        'this_month_child_incr':this_month_child.filter(created_on__month=date.today().month).count()*100/this_month_child.count(),
        'this_month_maralia':this_month_maralia.filter(created_on__month=date.today().month).count(),
        'this_month_maralia_incr':this_month_maralia.filter(created_on__month=date.today().month).count()*100/this_month_maralia.count(),
        'this_month_tube':this_month_tube.filter(created_on__month=date.today().month).count(),
        'this_month_tube_incr':this_month_tube.filter(created_on__month=date.today().month).count()*100/this_month_tube.count()
        }
    return render(request,'dashboard/home.html',context)

@is_health_center
def malnutrition(request):
    memebrs=request.user.clinic_members
    all_mal=Malnutrition.objects.filter(worker__in=memebrs,has_malnutrition=True)
    paginator=Paginator(all_mal, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context={
        "all_mal":page_obj,
        "page_number":page_number,
        "count":paginator.num_pages,
        "c_record":all_mal.count()
    }
    if request.method=='POST':
        start=request.POST.get('from')
        to=request.POST.get('to')
        all_mal=Malnutrition.objects.filter(worker__in=memebrs,has_malnutrition=True,created_on__range=[start,to])
        pdf=render_to_pdf('pdfs/malnutrition.html',{'count':all_mal.count(),'all_mal':all_mal,'today':date.today(),'start':start,'to':to})
        return HttpResponse(pdf,content_type='application/pdf')
    return render(request,'healtfeature/malnutrition.html',context)

@is_health_center
def contraception(request):
    memebrs=request.user.clinic_members
    all_mal=Contraception.objects.filter(worker__in=memebrs)
    paginator=Paginator(all_mal, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context={
        "all_mal":page_obj,
        "page_number":page_number,
        "count":paginator.num_pages,
        "c_record":all_mal.count()
    }
    if request.method=='POST':
        start=request.POST.get('from')
        to=request.POST.get('to')
        all_mal=Contraception.objects.filter(worker__in=memebrs,created_on__range=[start,to])
        pdf=render_to_pdf('pdfs/contraception.html',{'count':all_mal.count(),'all_mal':all_mal,'today':date.today(),'start':start,'to':to})
        return HttpResponse(pdf,content_type='application/pdf')
    return render(request,'healtfeature/contraception.html',context)

@is_health_center
def members(request):
    memebrs=request.user.clinic_members
    paginator=Paginator(memebrs, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context={
        "all_mal":page_obj,
        "page_number":page_number,
        "count":paginator.num_pages,
        "c_record":memebrs.count()
    }
    return render(request,'healtfeature/members.html',context)

@is_health_center
def patient(request):
    memebrs=request.user.clinic_members
    all_mal=Patient.objects.filter(worker__in=memebrs)
    paginator=Paginator(all_mal, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context={
        "all_mal":page_obj,
        "page_number":page_number,
        "count":paginator.num_pages,
        "c_record":all_mal.count()
    }
    if request.method=='POST':
        start=request.POST.get('from')
        to=request.POST.get('to')
        all_mal=Patient.objects.filter(worker__in=memebrs,created_on__range=[start,to])
        pdf=render_to_pdf('pdfs/patient.html',{'count':all_mal.count(),'all_mal':all_mal,'today':date.today(),'start':start,'to':to})
        return HttpResponse(pdf,content_type='application/pdf')
    return render(request,'healtfeature/patients.html',context)

@is_health_center
def house_hold(request):
    all_mal=HouseHold.objects.filter()
    paginator=Paginator(all_mal, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    village=Village.objects.all()
    form=HouseHoldForm()

    context={
        "all_mal":page_obj,
        "page_number":page_number,
        "count":paginator.num_pages,
        "c_record":all_mal.count(),
        'village':village,
        'form':form
        
    }
    if request.method=='POST':
        form=HouseHoldForm(request.POST)
        if form.is_valid():
            req=form.save(commit=False)
            req.worker=request.user
            req.save()
            messages.success(request, 'added successful ')
        context['form']=form
    elif request.GET.get("search"):
        name=request.GET.get("search")
        all_mal=HouseHold.objects.filter(Q(father_full_name__icontains=name)|Q(mother_full_name__icontains=name)|Q(phone_number__icontains=name))
        context['all_mal']=all_mal
    return render(request,'healtfeature/houseHold.html',context)