from django.urls import path
from .views import *

urlpatterns = [
    path('',login_page,name='login'),
    path('logout/',logout_page, name="logout_page"),
    path('recepie/',recepie),
    path('delete/<id>/', delete_recepie,name="delete"),
    path('update/<id>/',update_recepie,name="update"),
    path('register/',register_page),
]
  
 
