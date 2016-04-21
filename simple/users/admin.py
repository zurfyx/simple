from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'first_name', 'email', 'last_login')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('id', 'email', 'password',
                           'date_joined', 'last_login')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'birthday',
                                      'country', 'city', 'occupation')}),
        ('Permissions', {'fields': ('is_staff',)}),
        ('Platform', {'fields': ('role',)})
    )
    add_fieldsets = (
        (None, {'fields': ('id', 'email', 'password',
                           'date_joined', 'last_login')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'birthday',
                                      'country', 'city', 'occupation')}),
        ('Permissions', {'fields': ('is_staff',)}),
        ('Platform', {'fields': ('role',)})
    )
    readonly_fields = ('id', 'date_joined', 'last_login',)

    search_fields = ('id', 'email',)
    ordering = ('id',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)