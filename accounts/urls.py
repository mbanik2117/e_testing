from django.urls import path
from .views import SignupView, LoginView, LogoutView,SignupVerificationView, ResendVerificationCodeView, LoginVerificationView
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signup-verification/<int:user_id>/', SignupVerificationView.as_view(), name='signup_code_verification'),
    path('resend_verification_code/<int:user_id>/', ResendVerificationCodeView.as_view(), name='resend_verification_code'),
    path('login_verification/<int:user_id>/', LoginVerificationView.as_view(), name='login_verification'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
