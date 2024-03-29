import logging

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.edit import FormView

from .forms import ContactForm


class ContactView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    """
    Send a message to admin. Requires login
    """
    form_class = ContactForm
    template_name = "assignment/contact.html"

    login_url = '/assignment/login/'
    success_url = '/assignment/login/'
    success_message = "Email sent successfully"

    def form_valid(self, form):
        #send email from form, get message if it was successful
        email_sent_successfully = form.send_email(self.request.user.username)
        if not email_sent_successfully:
            self.success_message = "Email was not sent, please try again later"
        return super().form_valid(form)

class SignupView(FormView):
    """
    Sign up new users
    """

    form_class = UserCreationForm
    template_name = "assignment/signup.html"

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        #get created user
        try:
            user_test = User.objects.get(username=username)
        except User.DoesNotExist as ex:
            logger = logging.getLogger(__name__)
            logger.error('Freshly created user was not found in database, \
            + might be empty username. Full exception text: %s', ex)
            return redirect(reverse('assignment:signup'))
        #log in new user in his new account
        login(self.request, user_test)
        #redirect to contact page, because there is nothing to do in this app
        return redirect(reverse('assignment:contact'))

class LoginView(FormView):
    """
    Log in existing users
    """

    form_class = AuthenticationForm
    template_name = 'assignment/login.html'
    success_url = 'assignment/contact.html'

    def form_valid(self, form):
        #no exception because form handles it
        #login user data from form
        login(self.request, form.get_user())
        return redirect(reverse('assignment:contact'))
