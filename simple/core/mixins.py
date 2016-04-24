from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = 'users:login'
    redirect_field_name = 'next'
