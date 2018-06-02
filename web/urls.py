# -*- coding: utf8 -*-
from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookListView.as_view()),
    path('book/<int:pk>/', views.BookDetailView.as_view()),
    path('book/create/', views.BookCreate.as_view()),  
    path('book/<int:pk>/update/', views.BookUpdate.as_view()),  
    path('book/<int:pk>/delete/', views.BookDelete.as_view()),    
    path('reader/', views.ReaderListView.as_view()),
    path('reader/<int:pk>/', views.ReaderDetailView.as_view()),
    path('reader/create/', views.ReaderCreate.as_view()),  
    path('reader/<int:pk>/update/', views.ReaderUpdate.as_view()),    
    path('reader/<int:pk>/delete/', views.ReaderDelete.as_view()),
    path('circulate/step1/', views.Circulate1ListView.as_view()),
    path('circulate/step2/<int:reader_id>/', views.Circulate2ListView.as_view()),  
    path('circulate/step3/<int:reader_id>/<int:book_id>/', views.Circulate3DetailView.as_view()),
    path('return/step1/', views.Return1ListView.as_view()),
    path('return/step2/<int:book_id>/', views.Return2DetailView.as_view()),    
]