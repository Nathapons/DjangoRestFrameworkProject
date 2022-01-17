from . import views
from django.urls import path


urlpatterns = [
    path('service/', views.ServiceList.as_view(), name='show_all_service'),
]