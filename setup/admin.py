from django.contrib import admin
from .models import UserProfile, Exam, Subject, Question, Test, TestAttempt, UserAnswer

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

class ExamAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('exams',)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'test', 'created_at',)
    search_fields = ('text', 'test__name',)
    list_filter = ('test__name',)

class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'description',)
    search_fields = ('name', 'subject__name',)
    list_filter = ('subject__name',)

class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'subject', 'test', 'start_time', 'end_time', 'score',)
    search_fields = ('user_profile__user__username', 'subject__name',)
    list_filter = ('subject__name', 'test__name',)


class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('test_attempt', 'question', 'selected_option', 'created_at',)
    search_fields = ('test_attempt__user__user__username', 'question__text',)
    list_filter = ('test_attempt__subject__name', 'question__test__name', 'selected_option',)

# Register your models with the custom admin classes
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(TestAttempt, TestAttemptAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
