from django.shortcuts import render,reverse,redirect
import stripe 
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View 
from django.views.generic import TemplateView 
from django.http import JsonResponse,HttpResponse
from http import HTTPStatus
from membership.response import Response
from membership.handlers import StripeEventHandler
from .models import Membership
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

class SubscriptionPageView(TemplateView):
    template_name = "membership/subscription_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plans = Membership.objects.all()
        context['plans'] = plans
        return context
# Adding an endpoint on my server that creates a Checkout session that controls what your customer sees on the payment such as line items, the order amount and currency, and acceptable payment methods

# Checkout session provides a URL that redirects customers to a Stripe-hosted payment page
class CreateCheckoutSessionView(View):
    def post(self,request,*args,**kwargs):
        plan_id = self.kwargs["pk"]
        user_id = request.user.id
        plan = Membership.objects.get(id=plan_id)
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types =['card'],
                # items that are going to be purchased
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        "price_data":{
                            "currency" : "INR",
                            "unit_amount" : plan.price,
                            "product_data":{
                                "name" : "Sigma Library : {membership_type} Membership".format(membership_type = plan.membership_type),
                                "description" : "Become a {membership_type} Member".format(membership_type = plan.membership_type)
                            }
                        },
                        'quantity' : 1,
                    }
                ],
                metadata={
                    "plan_id":plan_id,
                    "user_id": user_id
                },
                mode='payment',
                success_url=settings.YOUR_DOMAIN + '/subscribe/success/',
                cancel_url=settings.YOUR_DOMAIN + '/subscribe/cancel/',
            )
        except Exception as e:
            print(e)
            return Response(status = HTTPStatus.FORBIDDEN)
        return redirect(checkout_session.url,code = 303)
        

class SuccessView(TemplateView):
    template_name = "membership/success.html" 
    
class CancelView(TemplateView):
    template_name = "membership/cancel.html"

@method_decorator(csrf_exempt,name="dispatch")
class StripeWebhookView(View):
    def post(self,request):
        payload = request.body
        signature = request.META['HTTP_STRIPE_SIGNATURE']
        handler = StripeEventHandler(payload,signature)
        handler.create_event()
        handler.execute_event()
        return HttpResponse()
        