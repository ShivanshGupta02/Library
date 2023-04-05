from django import forms
import datetime 
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _ 
from  .models import BookInstance

# class RenewBookForm(forms.Form):
    # renewal_date = forms.DateField(help_text="Enter a date b/w now and 4 weeks(default 3)")

    # def clean_renewal_date(self):
    #     data = self.cleaned_data['renewal_date']
        
    #     # check if date is not in the past
    #     if data < datetime.date.today():
    #         raise ValidationError(_('Invalid Date - Renewal in past'))
        
    #     # check in date is 4 week ahead
    #     if data > datetime.date.today() + datetime.timedelta(weeks=4):
    #         raise ValidationError(_('Invalid data - renewal more than 4 weeks ahead'))

    #     return data
    
import uuid
    
class IssueBookForm(forms.Form):
    username = forms.CharField()
    bookInstance_id = forms.UUIDField()
    due_back_date = forms.DateField(help_text="Enter a date b/w now and 4 weeks")
    
    def clean_due_back_date(self):
        data = self.cleaned_data['due_back_date']
        
        # check if date is not in the past
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - Past date'))
        
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid data - Due back date more than 4 weeks ahead'))
        
        return data
        
    def clean_username(self):
        data = self.cleaned_data['username']
        if not User.objects.filter(username=data).exists():
            raise ValidationError(_("Invalid username : Username doesn't exist"))   
        return data

    def clean_bookInstance_id(self):
        data = self.cleaned_data['bookInstance_id']
        if not BookInstance.objects.filter(id=data).exists():
            raise ValidationError(_("No book exists for given UUID"))
        obj = BookInstance.objects.filter(id=data)[0]
        if obj.status !=BookInstance.AVAILABLE :
            raise ValidationError(_("This book is not available to issue"))
        return data