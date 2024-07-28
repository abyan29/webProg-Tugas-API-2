from django.contrib import admin
from myFirstapp.models import *
# Register your models here.


@admin.register(AccountUser)
class AccountUser(admin.ModelAdmin):
    pass

@admin.register(Course)
class Course(admin.ModelAdmin):
    pass

@admin.register(AttendingCourse)
class AttendingCourse(admin.ModelAdmin):
    pass
