from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms

from users.constants import UserRoles
from .models import User


class UserCreationAdminForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=UserRoles.USER_ROLES)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'birthday', 'country',
                  'city', 'occupation', 'password1', 'password2', 'role',
                  'avatar')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeAdminForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    role = forms.ChoiceField(choices=UserRoles.USER_ROLES)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'birthday', 'country',
                  'city', 'occupation', 'role', 'avatar',)
        readonly_fields = ('email', 'date_joined', 'last_login',)

    def clean_password(self):
        return self.initial["password"]


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users.
    """
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'birthday', 'country',
                  'city', 'occupation', 'password1', 'password2', 'avatar')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users.
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'birthday', 'country',
                  'city', 'occupation', 'avatar',)
        readonly_fields = ('date_joined', 'last_login',)


