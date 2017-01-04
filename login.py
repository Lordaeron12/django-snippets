# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from wagtail.wagtailcore.models import Page, Site
from users.models import User

class LoginView(TemplateView):
    template_name = "users/login_signup.html"

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['page'] = Site.objects.get(pk=self.request.site.pk).root_page
        context['is_login'] = True
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')    
            else:
                msg = 'Usuario o contraseña incorrectas'           
        except Exception as e:
            msg = str(e)

        messages.add_message(request, messages.WARNING, msg)

        return redirect('login')
