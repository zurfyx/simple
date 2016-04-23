from django.contrib.auth import authenticate, login
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from users.forms import UserCreationForm


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = UserCreationForm
    success_url = '/'


class LoginView(TemplateView):
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
        # TODO redirect to success url if already-logged-in
        return super(LoginView, self).get(request, args, kwargs)

    def post(self, request, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            self.errors.append('Credentials are invalid')
        else:
            login(request, user)
        return super(LoginView, self).get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['errors'] = self.errors
        return context
