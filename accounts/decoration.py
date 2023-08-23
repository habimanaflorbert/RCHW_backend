from django.core.exceptions import PermissionDenied

from accounts.models import User


def is_health_center(function):
    def wrap(request, *args, **kwargs):
        if request.user.user_type ==User.HC:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap