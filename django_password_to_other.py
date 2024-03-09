#!/uar/bin/python3
# Purpose:
#   I have django app, My specification is that when I create user with django admin, 
#   I want to give username and password to someone else but in the time of logging in to 
#   the app with the provided credentials, the app will ask him or her to change password direct. how to achieve that in django?
# Solution:
#  You can achieve this in Django by customizing the authentication process using signals and views. Here's a general outline of how you can implement this:
#  Customize User Creation Signal: You'll want to listen for the post_save signal from the User model to trigger an action after a new user is created. When a new user is created via Django admin, you can send the username and temporary password to the designated person.

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

@receiver(post_save, sender=User)
def send_temporary_password(sender, instance, created, **kwargs):
    if created:
        # Send username and temporary password to designated person
        # You can use Django's mail or any other method to send this information
        temporary_password = 'generate a temporary password here'
        instance.set_password(temporary_password)
        instance.save()
        # Add the user to a group if needed
        # e.g., instance.groups.add(Group.objects.get(name='Temporary Password Users'))

#  Create a Custom Authentication Backend: You can create a custom authentication backend to intercept 
#  the login process and redirect users to a password change page if their password is temporary.

from django.contrib.auth.backends import ModelBackend
from django.shortcuts import redirect
from django.urls import reverse

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username, password, **kwargs)
        if user is not None and user.check_password(password):
            if user.has_temporary_password():
                # Redirect the user to a password change page
                return redirect(reverse('password_change'))
        return user

#  Password Change View: Create a view where users can change their password after logging in with a temporary password.

from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('password_change_done')

#
#  Update URLs: Add URL mappings for the password change view.
#

from django.urls import path
from .views import CustomPasswordChangeView

urlpatterns = [
    # Other URL patterns
    path('accounts/password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
]

#  Remember to replace 'generate a temporary password here' with your actual logic for generating temporary passwords 
#  and handle the email sending process appropriately.

#  This setup ensures that users are forced to change their password upon logging in with a temporary one provided by the administrator.
