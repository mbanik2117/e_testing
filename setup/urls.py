from django.urls import path
from . import views
from .views import profile_view, report_card
from .views import HomeView, TestsView, ContactView, TestDetailsView
from .views import featured_subjects, recent_tests, user_performance

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', profile_view, name='profile'),
    path('subject-list/', views.subject_list, name='subject_list'),
    path('exam_subjects/<int:exam_id>/', views.exam_subjects, name='exam_subjects'),
    path('subject-tests/<str:subject_name>/<int:test_id>/', views.subject_tests, name='subject_tests'),
    path('subject-test-list/<str:subject_name>/', views.subject_test_list, name='subject_test_list'),
    path('report_card/<int:attempt_id>/', report_card, name='report_card'),
    path('home/', HomeView.as_view(), name='home'),
    path('tests/', TestsView.as_view(), name='tests'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('test_details/<int:test_id>/', TestDetailsView.as_view(), name='test_details'),
    path('featured-subjects/', featured_subjects, name='featured_subjects'),
    path('recent-tests/', recent_tests, name='recent_tests'),
    path('user-performance/', user_performance, name='user_performance'),

]
