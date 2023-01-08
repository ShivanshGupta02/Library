from django.shortcuts import render
import stripe 
from django.conf import settings
from django.views import View 
from django.views.generic import TemplateView 
from django.http import JsonResponse
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY 

class SubscriptionPageView(TemplateView):
    template_name = "subscription_detail.html"

class CreateCheckoutSessionView(View):
    def post(self,request,*args,**kwargs):
        YOUR_DOMAIN = "https://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': '{{PRICE_ID}}',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
        )
        

