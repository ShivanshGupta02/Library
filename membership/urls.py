from django.contrib import admin
from django.urls import path 
from .views import *

urlpatterns = [
    path('',SubscriptionPageView.as_view(),name='subscription-page'),
    path('create-checkout-session/<int:pk>/',CreateCheckoutSessionView.as_view(),name='create-checkout-session'),
    path('success/',SuccessView.as_view(),name='success'),
    path('cancel/',CancelView.as_view(),name='cancel'),
    path('webhooks/stripe',StripeWebhookView.as_view(),name='stripe-webhook'),
]
