from django.contrib import admin
from django.urls import path
from Home import views

urlpatterns = [
    # ---------------- Root & Auth ---------------- #
    path("", views.index, name='Home'),
    path("LogIn", views.LogIn, name='LogIn'),
    path("SignUp", views.SignUp, name='SignUp'),
    path("LogInButton", views.LogInButton, name='LogInButton'),
    path("SignUpButton", views.SignUpButton, name='SignUpButton'),
    path("Logout", views.LogOut, name='Logout'),

    # ---------------- Core Pages ---------------- #
    path("Home", views.Home, name='Home'),
    path("ContactUs", views.ContactUs, name='ContactUs'),
    path("AboutUs", views.AboutUs, name='AboutUs'),
    path("Search", views.Search, name='Search'),

    # ---------------- Query / Answer ---------------- #
    path("AskingQuerry", views.AskingQuerry, name='AskingQuerry'),
    path("AnsweringQuery/<int:query_id>", views.Answer, name='AnsweringQuery'),
    path("Answered/<int:query_id>", views.Answered, name='Answered'),
    path("AllAnswers/<int:query_id>", views.AllAnswers, name='AllAnswers'),
    path("AllQueries", views.AllQueries, name='AllQueries'),
    path("unanswered/", views.unanswered_queries, name='unanswered_queries'),
    path("submit_rating/", views.SubmitRating, name='submit_rating'),

    # ---------------- Categories ---------------- #
    path("Categories:Attendance", views.Attendance, name='Attendance'),
    path("Categories:Miniproject", views.Miniproject, name='Miniproject'),
    path("Categories:Examination", views.Examination, name='Examination'),
    path("Categories:Practical_Viva", views.Practical_Viva, name='Practical_Viva'),
    path("Categories:Events", views.Events, name='Events'),
    path("Categories:Administration", views.Administration, name='Administration'),
    path("Categories:Others", views.Others, name='Others'),

    # ---------------- User ---------------- #
    path('user/<str:username>/queries/', views.user_queries, name='user_queries'),
]
