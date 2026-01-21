from django.contrib import admin
from student.models import StudentProfile
from teacher.models import TeacherProfile

# Register your models here.

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "student_class")
    search_fields = ("user__username", "user__first_name", "user__last_name")
    list_filter = ("student_class",)


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "subject", "classes")
    search_fields = ("user__username", "user__first_name", "user__last_name", "subject")