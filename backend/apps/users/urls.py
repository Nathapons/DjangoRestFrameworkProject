from . import views
from django.urls import path


urlpatterns = [
    # ----- User Login Function -------
    path('login_user/', views.UserLogin.as_view(), name='login_for_user'),
    path('login_technicians/', views.UserLogin.as_view(), name='login_for_technician'),
    path('login_admin/', views.UserLogin.as_view(), name='login_for_admin'),
    
    path('create_users/', views.CustomerCreate.as_view(), name='create_customer'),
    path('<int:id>/customerCRUD/', views.CustomerCrud.as_view(), name='crud_customer'),
]