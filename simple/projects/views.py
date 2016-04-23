from django.shortcuts import render
from django.views.generic import ListView

from .models import AbstractProjectRoles, AbstractProject


class ProjectList(ListView):
    """
    Display list of projects
    """
    model = AbstractProject
    template_name = 'projects/list.html'


class ProjectDetailList(ListView):
    """
    Display detail list of projects
    """
    model = AbstractProjectRoles
    template_name = 'projects/detail.html'
