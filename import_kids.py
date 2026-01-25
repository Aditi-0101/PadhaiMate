import csv
import os
import django

# Django setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PadhaiMate.settings")
django.setup()

from kid.models import Kid   # ✅ kid app

FILE_PATH = "kids.csv"

def run():
    print("📥 Importing kids data...")

    with open(FILE_PATH, newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        print("📌 CSV Headers detected:", reader.fieldnames)

        for row in reader:
            kid_id = row["username"].strip()          # LKG001
            name = f"{row['first_name']} {row['last_name']}".strip()
            class_raw = row["class"].strip()          # LKG

            # 🔹 Convert class like LKG → numeric
            CLASS_MAP = {
                "LKG": 0,
                "UKG": 1,
                "1": 1,
                "2": 2,
                "3": 3,
            }

            class_level = CLASS_MAP.get(class_raw, 0)

            kid, created = Kid.objects.get_or_create(
                kid_id=kid_id,
                defaults={
                    "name": name,
                    "class_level": class_level,
                }
            )

            if created:
                print(f"✅ Kid added: {kid_id}")
            else:
                print(f"⚠️ Kid already exists: {kid_id}")

    print("🎉 Kids import completed!")

if __name__ == "__main__":
    run()
