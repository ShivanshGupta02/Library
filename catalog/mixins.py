from django.core.exceptions import PermissionDenied 
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import reverse

class LoginRequiredMixin(AccessMixin):
    login_url = 'signin'  # Update the URL path to your login page

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            # Redirect to login page
            return redirect(reverse(self.login_url))
        return super().handle_no_permission()


class CheckStaffGroupMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="Staff Members").exists():
            return super().dispatch(request, *args, **kwargs)
        
        else:
            raise PermissionDenied