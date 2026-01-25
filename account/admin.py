from django.contrib import admin
from student.models import StudentProfile
from teacher.models import TeacherProfile
from kid.models import Kid

# Register your models here.

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "student_class")
    search_fields = ("user__username", "user__first_name", "user__last_name")
    list_filter = ("student_class",)


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "subject", "classes")
    search_fields = ("user__username", "user__first_name", "user__last_name", "subject")\
    
@admin.register(Kid)
class KidAdmin(admin.ModelAdmin):
    list_display = ('kid_id', 'name', 'class_level')
    list_filter = ('class_level',)
    search_fields = ('kid_id', 'name')