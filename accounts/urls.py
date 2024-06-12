from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    path('token/access/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('student/', views.StudentView.as_view()),
    path('student/<int:pk>/', views.StudentView.as_view())
]
