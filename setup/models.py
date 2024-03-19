from django.db import models
from accounts.models import UserProfile


class Exam(models.Model):
    name = models.CharField(max_length=255)


class Subject(models.Model):
    name = models.CharField(max_length=20)
    exams = models.ManyToManyField(Exam)


class Test(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.TextField()
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correct_option = models.CharField(max_length=1)  # A, B, C, or D
    created_at = models.DateTimeField(auto_now_add=True)  # Add a timestamp for each question creation

    def get_options_with_numbers(self):
        """Returns a list of tuples representing the options and their letters (A, B, C, D)."""
        return [
            ('A', self.option1),
            ('B', self.option2),
            ('C', self.option3),
            ('D', self.option4),
        ]


class TestAttempt(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)  # Set start time automatically
    end_time = models.DateTimeField(null=True)  # Set end time when test is submitted
    score = models.IntegerField(null=True)

    def __str__(self):
        return f"TestAttempt {self.id} - {self.user_profile}"


class UserAnswer(models.Model):
    test_attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Add a timestamp for each answer
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"UserAnswer - {self.id} - {self.user_profile}"
