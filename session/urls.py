from django.urls import path
from . import views

urlpatterns = [

    # all session operation
    path('session/', views.SessionView.as_view()),
    path('session/<int:pk>/', views.SessionView.as_view()),

    # add or delete students from sesssion
    path('session/<int:session_pk>/student/<str:student_uuid>/', views.SessionStudentsView.as_view())
]
