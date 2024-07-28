import sys
from django.contrib import messages
from django.db.models.signals import post_save
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.contrib.auth.models import User
from myFirstapp.models import AccountUser, Course, AttendingCourse
from myFirstapp.signals import check_nim
from myFirstapp.forms import StudentRegisterForm
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    return render(request='home.html')

def readCourse(request):
    #mengambil data dari models.py yang Course
    data = Course.objects.filter()[:1]
                                   
    konteks = {'data list' : data}

    return render(request,'course.html', konteks)

def createCourse(request):
    return render(request,'home.html')


def updateCourse(request):
    return render(request,'home.html')

@csrf_protect
def deleteCourse(request):
    data = Course.objects.get(course_id=id)
    if User:
        data.delete()
        messages.success(request,'data berhasil di hapus')
        return redirect('myFirstapp:read-data-course')
    else:
         messages.success(request, 'Data Tidak ada')
         return redirect('myFirstapp:read-data-course')


def readStudent(request):
    #mengambil data dari models.py yang Accountuser
    data = AccountUser.objects.all()

    context = {'data_list': data}

    return render(request, 'index.html', context)


@csrf_protect
def createStudent(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            post_save.disconnect(check_nim)
            form.fullname = form.cleaned_data.get("fullname")
            form.nim = form.cleaned_data.get("nim")
            form.email = form.cleaned_data.get("email")
            post_save.send(
                sender=AccountUser,created=None,instance=form, dispatch_uid="cheack nim")
            messages.success(request, 'Data berhasil disimpan')
            return redirect('myFirstapp:read-data-student')
    else:
        form = StudentRegisterForm()
    return render(request, 'home.html', {'form':form})
        

@csrf_protect
def updateStudent(request, id):
    member = get_object_or_404(AccountUser, account_user_related_user=id)
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Berhasil diupdate')
            return redirect('myFirstapp:read-data-student')
    else:
        form = StudentRegisterForm(initial={
            'account_user_fullname':member.account_user_fullname,
            'account_user_student_number':member.account_user_student_number,
            'account_user_email':member.account_user_email,
        })
    return render(request, 'update.html', {'form':form})



@csrf_protect
def deleteStudent(request, id):
    member = AccountUser.objects.get(account_user_related_user=id)
    user = User.objects.get(username=id)
    member.delete()
    user.delete()
    messages.success(request, 'Data Berhasil dihapus')
    return redirect('myFirstapp:read-data-student')







