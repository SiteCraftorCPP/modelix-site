from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('submit-order/', views.submit_order, name='submit_order'),
    path('submit-call-request/', views.submit_call_request, name='submit_call_request'),
]
