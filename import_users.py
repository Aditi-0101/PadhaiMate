import csv
import os
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PadhaiMate.settings')
django.setup()

from django.contrib.auth.models import User
from student.models import StudentProfile
from teacher.models import TeacherProfile


# -------- IMPORT STUDENTS --------
with open('students.csv', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        user, created = User.objects.get_or_create(
            username=row['username'],
            defaults={'password': row['password'],
                      'first_name': row['first_name'],
                        'last_name': row['last_name'],
                    }
        )

        if created:
            user.set_password(row['password'])
            user.is_staff = False
            user.save()
            print(f"Student user created: {row['username']}")
        else:
            user.first_name = row['first_name']
            user.last_name = row['last_name']
            user.save()
            print(f"Student user already exists: {row['username']}")

        # 🔴 IMPORTANT: profile check
        if not hasattr(user, 'student_profile'):
            StudentProfile.objects.create(
                user=user,
                student_class=int(row['class'])
            )
            print(f"Student profile created for: {row['username']}")


# -------- IMPORT TEACHERS --------
with open('teachers.csv', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        user, created = User.objects.get_or_create(
            username=row['username'],
            defaults={'password': row['password'],
                      'first_name': row['first_name'],
                      'last_name': row['last_name']
                    }
        )

        if created:
            user.set_password(row['password'])
            user.is_staff = True
            user.save()
            print(f"Teacher user created: {row['username']}")
        else:
            user.first_name = row['first_name']
            user.last_name = row['last_name']
            user.save()
            print(f"Teacher user already exists: {row['username']}")

        # 🔴 IMPORTANT: profile check
        if not hasattr(user, 'teacher_profile'):
            TeacherProfile.objects.create(
                user=user,
                subject=row['subject'],
                classes=row.get('class', '')
            )
            print(f"Teacher profile created for: {row['username']}")
