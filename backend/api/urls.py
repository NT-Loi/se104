from django.urls import path
from .views import *

urlpatterns = [
    path('sach/', SachListCreate.as_view(), name='sach-list'),
    path('sach/delete/<int:pk>/', SachDelete.as_view(), name='delete-sach'),
]
