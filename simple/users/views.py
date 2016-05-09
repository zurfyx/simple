from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from users.forms import UserCreationForm
from users.mixins import NotLoginRequiredMixin
from users.models import User


class RegisterView(NotLoginRequiredMixin, CreateView):
    template_name = 'users/register.html'
    form_class = UserCreationForm
    success_url = '/'


class LoginView(NotLoginRequiredMixin, TemplateView):
    """
    Login View, custom form handling related with a custom .html template
    Fields are email and password, both gathered by POST.
    Errors list like {{ errors }}
    """
    template_name = 'users/login.html'
    success_url = '/'

    def __init__(self, **kwargs):
        super(LoginView, self).__init__(**kwargs)
        self.errors = []

    def get(self, request, *args, **kwargs):
        return super(LoginView, self).get(request, args, kwargs)

    def post(self, request, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            self.errors.append('Credentials are invalid')
        else:
            login(request, user)
            return redirect('/')
        return super(LoginView, self).get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['errors'] = self.errors
        return context


class AccountView(DetailView):
    template_name = 'users/account.html'
    model = User
    context_object_name = 'context_user'


class UserList(ListView):
    """
    Display user's lists.
    Everybody can see all users.
    """
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'


class SearchUser(ListView):
    """
    Display user search.
    If an user input the user's firstname, it shows users with this name. Else if, it shows No Results
    """
    model = User
    context_object_name = 'users'
    template_name = '/users/list.html'


    def get_queryset(self):
        filter = self.kwargs['first-name']
        search= self.model.objects.filter(firstname__icontains = filter)
        return search