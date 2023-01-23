from django.conf import settings 
from membership.functions import create_user_subscription
import stripe 
from django.core.mail import send_mail
from .models import Membership
class StripeEventHandler:
    def __init__(self,payload,sig_header)-> None:
        self.payload = payload
        self.signature = sig_header 
    
    def create_event(self):
        try:
            self.event = stripe.Webhook.construct_event(
                self.payload, 
                self.signature,
                settings.STRIPE_WEBHOOK_KEY,
                )
            return True 
        
        except ValueError as e:
            # Invalid payload
            print(e)
        
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            print(e)
        
        return False
    
    
    def execute_event(self):
        try:
            event_type = self.event.get("type")
            if event_type == "checkout.session.completed":
                self._checkout_session_completed()
            elif event_type == 'checkout.session.async_payment_failed':
                self._checkout_session_payment_failed()
            elif event_type == 'checkout.session.async_payment_succeeded':
                self._checkout_session_payment_succeeded()
        
        except Exception as e:
            print(e)
            
    def _checkout_session_completed(self):
        session = self.event["data"]["object"]
        print("`Checkout session completed` : ",session)
        print("checkout compeleted triggered")
        if session["payment_status"] == 'paid':
            print("payment paid triggered")
            self._checkout_fulfillment(session)
            
    def _checkout_session_payment_succeeded(self):
        session = self.event["data"]["object"]
        print("Checkout session payment succeeded :",session)
        self._checkout_fulfillment(session)
        
    def _checkout_session_payment_failed(self,session):
        print("Payment failed")
        session = self.event["data"]["object"]
        # TODO : sent a mail to user that his subscription payment is failed
        
    def _checkout_fulfillment(self,session):
        print("fulfillment triggered")
        metadata = session ['metadata']
        user_id = metadata.get('user_id')
        plan_id = metadata.get("plan_id")
        membership_type = Membership.objects.get(id=plan_id).membership_type
        create_user_subscription(
            dict(
                membership_id = plan_id,
                user_id = user_id,
            ),
            payment_confirm=True
        )