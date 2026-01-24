from django.contrib import admin
from .models import Question, AssessmentResult

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "class_level",
        "subject_name",
        "difficulty",
        "short_question",
    )
    list_filter = ("class_level", "subject_name", "difficulty")
    search_fields = ("question_text",)

    def short_question(self, obj):
        return obj.question_text[:50] + "..."


@admin.register(AssessmentResult)
class AssessmentResultAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "subject_name",
        "easy_correct",
        "medium_correct",
        "hard_correct",
        "created_at",
    )
    list_filter = ("subject_name", "created_at")
