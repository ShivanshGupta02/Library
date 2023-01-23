from django.core.exceptions import PermissionDenied 

class CheckStaffGroupMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="Staff Members").exists():
            return super().dispatch(request, *args, **kwargs)
        
        else:
            raise PermissionDenied