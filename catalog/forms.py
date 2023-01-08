from django import forms
import datetime 
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _ 

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date b/w now and 4 weeks(default 3)")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        
        # check if date is not in the past
        if data < datetime.date.today():
            raise ValidationError(_('Invalid Date - Renewal in past'))
        
        # check in date is 4 week ahead
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid data - renewal more than 4 weeks ahead'))

        return data
    