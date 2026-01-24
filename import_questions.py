import csv
from student.models import Question

with open("question_bank_with_topics.csv", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        Question.objects.create(
            class_level=int(row["class"]),
            subject_name=row["subject_name"],
            topic_name=row["topic_name"],
            difficulty=row["difficulty"],
            question_text=row["question_text"],
            option_a=row["option_a"],
            option_b=row["option_b"],
            option_c=row["option_c"],
            option_d=row["option_d"],
            correct_option=row["correct_option"],
        )

print("Questions imported successfully")
