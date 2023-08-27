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
from home.models import *
from accounts.models import Village,UserAddress
from healthCenter.forms import HouseHoldForm,BirthChildForm,PregnancyForm
from healthCenter.models import *
from accounts.forms import *

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
    elif request.GET.get("search"):
        name=request.GET.get("search")
        all_mal=Malnutrition.objects.filter(Q(child_full_name__icontains=name)|Q(family__father_full_name__icontains=name)|Q(family__mother_full_name__icontains=name))
        context['all_mal']=all_mal
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
    elif request.GET.get("search"):
        name=request.GET.get("search")
        all_mal=Contraception.objects.filter(Q(family__father_full_name__icontains=name)|Q(family__mother_full_name__icontains=name))
        context['all_mal']=all_mal
    return render(request,'healtfeature/contraception.html',context)

@is_health_center
def members(request):
    memebrs=request.user.clinic_members
    paginator=Paginator(memebrs, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    form=UmujyanamaForm()
    villages=Village.objects.filter(sector=request.user.clinic_address.sector)

    context={
        "all_mal":page_obj,
        "page_number":page_number,
        "count":paginator.num_pages,
        "c_record":memebrs.count(),
        "form":form,
        "villages":villages
    }
    if request.GET.get("search"):
        name=request.GET.get("search")
        all_mal=memebrs.objects.filter(Q(full_name__icontains=name)|Q(phone_number__icontains=name))
        context['all_mal']=all_mal

    elif request.method=='POST':
        form=UmujyanamaForm(request.POST)
        if form.is_valid():
            req=form.save(commit=False)
            new_pass=get_random_string(8)
            req.password=new_pass
            req.username=request.POST['phone_number']
            req.save()
            request.user.clinic.members.add(req)
            village=Village.objects.get(id=request.POST['village'])
            UserAddress.objects.create(user=req,village=village)
            message=f"Hello dear {req.full_name} !\nYou have granted permission as Umujyanama wubuzima on mobile app as worker of{request.user.full_name} here's crendetials:\n username:{req.username} \n password:{new_pass} \n please change password after login to the system \n Thank you for using RCHW.  "
            subj="You have granted to be umujyanama wubuzima"
            send_mail_task(message,subj,req.email)
            messages.success(request, 'added successful ')
        context['form']=form
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

@is_health_center
def birth_child(request):
    all_mal=BirthChild.objects.filter(clinic=request.user)
    paginator=Paginator(all_mal, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    village=Village.objects.all()
    form=BirthChildForm()

    context={
        "all_mal":page_obj,
        "page_number":page_number,
        "count":paginator.num_pages,
        "c_record":all_mal.count(),
        'village':village,
        'form':form
    }
    
    if request.method=='POST' and request.GET.get('family'):
        try:
            family=HouseHold.objects.get(id=request.GET.get('family'))
            form=BirthChildForm(request.POST)
            if form.is_valid():
                req=form.save(commit=False)
                req.clinic=request.user
                req.family=family
                req.save()
                messages.success(request, 'Added successful ')
                context['form']=form
        except:
            pass
        return render(request,'healtfeature/birthChild.html',context)

    elif request.GET.get('family') and request.method =='GET':
        return render(request,'healtfeature/birthChild.html',context)
    elif request.method=='POST':
        start=request.POST.get('from')
        to=request.POST.get('to')
        all_mal=BirthChild.objects.filter(clinic=request.user,created_on__range=[start,to])
        pdf=render_to_pdf('pdfs/birth.html',{'count':all_mal.count(),'all_mal':all_mal,'today':date.today(),'start':start,'to':to})
        return HttpResponse(pdf,content_type='application/pdf')
    
    elif request.GET.get("search"):
        name=request.GET.get("search")
        all_mal=BirthChild.objects.filter(Q(full_name__icontains=name)|Q(family__father_full_name__icontains=name)|Q(family__mother_full_name__icontains=name))
        context['all_mal']=all_mal
    return render(request,'healtfeature/birthChildren.html',context)
    
    
@is_health_center
def pregnancy_woman(request):
    all_mal=Pregnancy.objects.filter()
    paginator=Paginator(all_mal, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    village=Village.objects.all()
    form=PregnancyForm()

    context={
        "all_mal":page_obj,
        "page_number":page_number,
        "count":paginator.num_pages,
        "c_record":all_mal.count(),
        'village':village,
        'form':form
        
    }
    if request.method=='POST':
        form=PregnancyForm(request.POST)
        if form.is_valid():
            req=form.save(commit=False)
            req.clinic=request.user
            req.save()
            messages.success(request, 'Added successful ')
        context['all_mal']=Pregnancy.objects.filter()
        context['form']=form
    elif request.GET.get("search"):
        name=request.GET.get("search")
        all_mal=Pregnancy.objects.filter(Q(full_name__icontains=name)|Q(phone__icontains=name))
        context['all_mal']=all_mal
    return render(request,'healtfeature/pregnancy.html',context)

def edit_pregnancy(request,pk):
    try:
        all_mal=Pregnancy.objects.get(id=pk)
        form=PregnancyForm(instance=all_mal)
        context={
        "inst":all_mal,
        'form':form
         }
        if request.method=='POST':
            form=PregnancyForm(request.POST,instance=all_mal)
            if form.is_valid():
                form.save(commit=True)
                messages.success(request, 'Updated successful')
    except Pregnancy.DoesNotExist:
        pass
    return render(request,'healtfeature/editPregnancy.html',context)

def delete_pregnancy(request,pk):
    try:
        all_mal=Pregnancy.objects.get(id=pk)
        all_mal.delete()
        messages.success(request, 'delete successful')
    except Pregnancy.DoesNotExist:
        pass
    return redirect('pregnancy_woman')


def edit_birth(request,pk):
    try:
        all_mal=BirthChild.objects.get(id=pk)
        form=BirthChildForm(instance=all_mal)
        context={
        "inst":all_mal,
        'form':form
         }
        if request.method=='POST':
            form=BirthChildForm(request.POST,instance=all_mal)
            if form.is_valid():
                form.save(commit=True)
                messages.success(request, 'Updated successful')
    except Pregnancy.DoesNotExist:
        pass
    return render(request,'healtfeature/editBirth.html',context)


def delete_birth(request,pk):
    try:
        all_mal=BirthChild.objects.get(id=pk)
        all_mal.delete()
        messages.success(request, 'delete successful')
    except BirthChild.DoesNotExist:
        pass
    return redirect('birth_child')

def settings(request):
    return render(request,'auth/settings.html')
