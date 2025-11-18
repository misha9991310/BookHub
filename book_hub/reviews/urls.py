from django.urls import path

from book_hub.books import views

urlpatterns = [path("", views.index, name="index")]
