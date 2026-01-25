import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PadhaiMate.settings")
django.setup()

from django.contrib.auth.models import User
from kid.models import Kid

with open("kids.csv", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    print("CSV HEADERS 👉", reader.fieldnames)

    for row in reader:
        username = row["username"].strip()
        password = row["password"].strip()
        first_name = row["first_name"].strip()
        last_name = row["last_name"].strip()
        class_level = row["class"].strip()

        # ---- USER ----
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
            }
        )

        # password hamesha set karo (safe)
        user.set_password(password)
        user.is_staff = False
        user.save()

        if created:
            print(f"✅ Kid user created: {username}")
        else:
            print(f"⚠️ Kid user already exists: {username}")

        # ---- KID PROFILE ----
        Kid.objects.get_or_create(
            user=user,
            kid_id=username,
            defaults={
                "name": f"{first_name} {last_name}",
                "class_level": class_level
            }
        )

print("🎉 Kids import completed successfully")
