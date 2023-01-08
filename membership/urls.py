from django.contrib import admin
from django.urls import path 
from .views import *

urlpatterns = [
    path('create-checkout-session/',CreateCheckoutSessionView.as_view(),name='create-checkout-session'),
    path('subscribe',SubscriptionPageView.as_view(),name='subscription-page')
]
