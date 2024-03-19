from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Subject, Question, TestAttempt, UserAnswer
from .models import Subject, Question, Exam, Test, TestAttempt
from accounts.models import UserProfile
from datetime import datetime as dt
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.views import View
from django.db.models import Window , F
from django.db.models.functions import Rank
from django.views.decorators.cache import cache_page

User = get_user_model()


@login_required
def profile_view(request):
    return render(request, 'profile.html')


@cache_page(60 * 30) 
@login_required
def home(request):
    if request.user.is_authenticated:
        user_profile = request.user.userprofile
        featured_subjects = Subject.objects.filter(test__testattempt__user_profile=user_profile).distinct()
        recent_tests = TestAttempt.objects.filter(user_profile=user_profile, end_time__isnull=False).order_by('-end_time')[:5]
        leaderboard = TestAttempt.objects.filter(user_profile=user_profile).order_by('-score')[:5]

        return render(request, 'home.html', {
            'authenticated': True,
            'featured_subjects': featured_subjects,
            'recent_tests': recent_tests,
            'leaderboard': leaderboard,
        })
    else:
        exams = Test.objects.all()  # You need to adjust this based on your model structure
        return render(request, 'home.html', {
            'authenticated': False,
            'exams': exams,
        })
    
@cache_page(60 * 30)  
@login_required
def subject_list(request):
    subjects = Subject.objects.all()
    exams = Exam.objects.all()
    context = {'subjects': subjects, 'exams': exams}
    return render(request, 'subject_list.html', context)

@login_required
def subject_tests(request, subject_name, test_id):
    subject = get_object_or_404(Subject, name=subject_name)
    test = get_object_or_404(Test, id=test_id, subject=subject)
    questions = Question.objects.filter(test=test).order_by('?')

    try:
        user_profile = UserProfile.objects.get(user=request.user)

        # Check if a TestAttempt already exists for the user, subject, and test
        test_attempt, created = TestAttempt.objects.get_or_create(
            user_profile=user_profile,
            subject=subject,
            test=test,
            end_time=None
        )

        if request.method == 'POST':
            for question in questions:
                selected_option = request.POST.get(f'answer_{question.id}')
                
                # Check if an answer was provided for the question
                if selected_option is not None:
                    UserAnswer.objects.create(
                        test_attempt=test_attempt,
                        question=question,
                        selected_option=selected_option,
                        user_profile=user_profile
                    )
                else:
                    # If no answer provided, assign a score of zero for that question
                    UserAnswer.objects.create(
                        test_attempt=test_attempt,
                        question=question,
                        selected_option=None,
                        user_profile=user_profile
                    )

            test_attempt.end_time = dt.now()
            test_attempt.save()

            report_card_url = reverse('report_card', kwargs={'attempt_id': test_attempt.id})
            return redirect(report_card_url)

    except UserProfile.DoesNotExist:
        # If the user profile does not exist, redirect to login
        return redirect('login')

    context = {
        'subject': subject,
        'test': test,
        'questions': questions,
        'test_duration': 120,
        'test_attempt': test_attempt,
    }
    return render(request, 'subject_test.html', context)



@cache_page(60 * 30) 
@login_required
def exam_subjects(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    subjects = Subject.objects.filter(exams=exam)
    context = {'subjects': subjects, 'exam': exam}
    return render(request, 'exam_subjects.html', context)


@cache_page(60 * 30) 
@login_required
def subject_test_list(request, subject_name):
    subject = get_object_or_404(Subject, name=subject_name)
    tests = Test.objects.filter(subject=subject)
    context = {'subject': subject, 'tests': tests}
    return render(request, 'subject_test_list.html', context)


@login_required
def report_card(request, attempt_id):
    attempt = TestAttempt.objects.get(id=attempt_id)
    user_answers = UserAnswer.objects.filter(test_attempt=attempt)

    # Compute the score and correct answers
    total_questions = user_answers.count()
    correct_answers = 0

    for user_answer in user_answers:
        if user_answer.selected_option == user_answer.question.correct_option:
            correct_answers += 1

    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

    # Update the attempt with the computed score
    attempt.score = score
    attempt.save()

    context = {
        'attempt': attempt,
        'user_answers': user_answers,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'score': score,
    }

    return render(request, 'report_card.html', context)

 
class HomeView(View):
    def get(self, request):
        exams = Exam.objects.all()
        return render(request, 'home.html', {'exams': exams})


class TestsView(View):
    def get(self, request):
        exams = Exam.objects.all()
        return render(request, 'tests.html', {'exams': exams})



class ContactView(View):
    def get(self, request):
        # You can pass any context data or contact details here
        return render(request, 'contact.html')

     
class TestDetailsView(View):
    template_name = 'subject_test_list.html'  # Change this to the appropriate template

    def get(self, request, test_id):
        test = get_object_or_404(Test, id=test_id)

        # Check if the user is authenticated
        if request.user.is_authenticated:
            # You can customize this context based on what information you want to display
            context = {
                'test': test,
            }

            return render(request, self.template_name, context)
        else:
            # Redirect to the login page if the user is not authenticated
            login_url = reverse('login')  # Assuming the name of your login URL is 'login'
            return redirect(login_url)



@cache_page(60 * 30) 
@login_required
def featured_subjects(request):
    user_profile = request.user.userprofile
    featured_subjects = Subject.objects.filter(test__testattempt__user_profile=user_profile).distinct()
    return render(request, 'featured_subjects.html', {'featured_subjects': featured_subjects})


@cache_page(60 * 30) 
@login_required
def recent_tests(request):
    user_profile = request.user.userprofile
    recent_tests = TestAttempt.objects.filter(user_profile=user_profile, end_time__isnull=False).order_by('-end_time')[:5]
    return render(request, 'recent_tests.html', {'recent_tests': recent_tests})



@cache_page(60 * 30) 
@login_required
def user_performance(request):
    user_profile = request.user.userprofile
    leaderboard = (
        TestAttempt.objects
        .filter(user_profile=user_profile)
        .order_by('-score')
        .annotate(rank=Window(expression=Rank(), order_by=F('score').desc()))
        [:5]
    )
    return render(request, 'user_performance.html', {'leaderboard': leaderboard})
