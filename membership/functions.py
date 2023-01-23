from .models import UserMembership
from membership.enums import PaymentStatus

def create_user_subscription(data,payment_confirm = False):
    print("create user subscription function triggered")
    try:
        if payment_confirm:
            data["payment_status"] = PaymentStatus.PAID.value 
            UserMembership.objects.create(**data)
            print("usermembership object created")
    
    except Exception as e:
        print(e)
    
    return None 
