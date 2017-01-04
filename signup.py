from django.contrib import messages #Messages framework for in-template alerts
from django.contrib.auth.hashers import make_password #Hash a string to encrypt a raw password 
from django.db import IntegrityError #Exception for db issues with constraints and integrity, like duplicated data
from django.shortcuts import redirect 
from django.views.generic import TemplateView
from users.models import User #App's auth user model
class SignupView(TemplateView):
    template_name = "users/signup.html"
    def post(self, request, *args, **kwargs):
        redirect_url = 'signup'
        try:
            email = request.POST['email']
            password = request.POST['password']
            password = make_password(password)
            user = User(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                telephone_number = request.POST['telephone_number'],
                id_type = request.POST['id_type'],
                id_number = request.POST['id_number'],
                email = email,
                username = email,
                password = password
            )
            user.save()
        except KeyError:
            msg = 'Some required fields are empty'
            tag = messages.WARNING
        except IntegrityError:
            msg = 'The user already exists'
            tag = messages.WARNING
        except Exception as e:
            msg = 'Error: ' + str(e)
            tag = messages.WARNING
        else:
            msg = '¡Success!'
            tag = messages.SUCCESS
            redirect_url = 'login'
        messages.add_message(request, tag, msg)
        
        return redirect(redirect_url)
