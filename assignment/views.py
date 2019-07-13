from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic

from .forms import ContactForm

class ContactView(LoginRequiredMixin, generic.edit.FormView):
    """
    Send a message to admin. Requires login
    """

    form_class = ContactForm

    #override default template name
    template_name = "assignment/contact.html"
    #override default login page location, triggers if unauthorised user
    #tried to access this page (LoginRequiredMixin)
    login_url = '/assignment/login/'
    #TODO: create success page
    success_url = '/assignment/login/'
    #TODO: is_valid send email to admin
    # self.request
    #TODO: add comments to this
    def form_valid(self, form):
        # print(self.request.user.username)
        form.send_email(self.request.user.username)
        #TODO:remove print
        return super().form_valid(form)

class SignupView(generic.edit.FormView):
    """
    Sign up new users
    """
    
    #use template form for user creation
    form_class = UserCreationForm
    #override default template name
    template_name = "assignment/signup.html"

    #if form is valid
    def form_valid(self, form):
        form.save()
        #get data from form
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password')
        #create new user
        #TODO: exception on authenticate from auth tutorial
        user = authenticate(username=username, raw_password=raw_password)
        #log in new user in his new account
        login(self.request, user)
        #redirect to contact page, because there is nothing to do in this app
        return redirect(reverse('assignment:contact'))

class LoginView(generic.edit.FormView):
    """
    Log in existing users
    """
    #TODO: if not logged in user was redirected here from
    # contact view, show message like "you must be logged in to send messages"
    
    form_class = AuthenticationForm
    template_name = 'assignment/login.html'
    success_url = 'assignment/contact.html'
    
    #if form is valid
    def form_valid(self, form):
        #no exception because form handles it
        #login user data from form
        login(self.request, form.get_user())
        return redirect(reverse('assignment:contact'))
