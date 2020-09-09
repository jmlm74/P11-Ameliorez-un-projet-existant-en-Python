import requests
from django.conf import settings as conf_settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from sentry_sdk.integrations import logging

from home_app.models import Translation
from user_app import forms
from .models import User


def user_create(request):
    """
    The creation form

    Validate the form and then connect the user with "authenticate" method or
    create the new user with "create" method
    """
    context = {'title': 'user_app-create-title'}
    if request.method == 'POST':
        userform = forms.UserPurBeurreForm(data=request.POST)
        if userform.is_valid():
            user = request.POST.copy()
            username = user["email"].split("@")[0]
            email = user["email"]
            password = user["password"]
            if "connexion" in request.POST:  # connection
                user = authenticate(username=username, password=password)
                if user:    # authenticated ?
                    if user.is_active:
                        login(request, user)
                        print(f"Connection of {username}")      # for the logs
                        try:
                            logging.info(f"connection of {user}")   # sentry
                        except AttributeError:
                            pass                        
                        return HttpResponseRedirect(reverse('home_app:index'))  # return to the index
                    else:
                        userform.add_error(None, "Compte désactivé : Connexion refusée")  # incactive
                else:
                    print(f"Someone try to login and failed ! user : {username} - psw : {password}")
                    userform.add_error(None, "Erreur de connexion : email/mot de passe erroné")  # connection error
            else:  # creation
                print(f"Register new user : {username} - {email}")
                new_user = User.objects.create_user(username, email, password)
                userform = forms.UserPurBeurreForm()
        else:  # form no valid
            print("Error on creation/connection form : {userform.errors}")
    else:  # not post but HTTP REQUEST
        userform = forms.UserPurBeurreForm()
    context['userform'] = userform
    return render(request, 'registration/create_user.html', context=context)


def user_login(request):
    """
    The creation/conncetion form (the same view)

    Validate the form and then connect the user with "authenticate" method or
    create the new user with "create" method
    """
    context = {}
    if request.method == 'POST':
        userform = forms.UserPurBeurreForm(data=request.POST)
        if userform.is_valid():
            user = request.POST.copy()
            username = user["email"].split("@")[0]
            email = user["email"]
            password = user["password"]
            if "connexion" in request.POST:  # connection
                user = authenticate(username=username, password=password)
                if user:    # authenticated ?
                    if user.is_active:
                        login(request, user)
                        print(f"Connection of {username}")      # for the logs
                        try:
                            logging.info(f"connection of {user}")   # sentry
                        except AttributeError:
                            pass
                        return HttpResponseRedirect(reverse('home_app:index'))  # return to the index
                    else:
                        userform.add_error(None, "Compte désactivé : Connexion refusée")  # incactive
                else:
                    print(f"Someone try to login and failed ! user : {username} - psw : {password}")
                    userform.add_error(None, "Erreur de connexion : email/mot de passe erroné")  # connection error
            else:  # creation
                print(f"Register new user : {username} - {email}")
                new_user = User.objects.create_user(username, email, password)
                userform = forms.UserPurBeurreForm()
        else:  # form no valid
            print("Error on creation/connection form : {userform.errors}")
    else:  # not post but HTTP REQUEST
        userform = forms.UserPurBeurreForm()
    context['title'] = "user_app-login-title"
    context['userform'] = userform
    return render(request, 'registration/login.html', context=context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home_app:index'))


@login_required
def change_password(request):
    context = {'title': 'user_app-change-psw-title'}
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_app:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    context['form'] = form
    return render(request, 'registration/change_password.html', context=context)


def reset_psw(request):
    context = {'title': "user_app-reset-title"}
    language = request.session['language']
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            clean_mail = form.cleaned_data['email']
            users = User.objects.filter(Q(email=clean_mail))
            if users.exists():
                for user in users:
                    subject = Translation.get_translation("Password Reset Requested", language)
                    email_template_name = f"registration/reset_password_email_{language}.txt"
                    if not conf_settings.PRODUCTION:
                        domain = "127.0.0.1:8000"
                        protocol = "http"
                    else:
                        domain = "purbeurre.jm-hayons74.fr"
                        protocol = "https"
                    c = {
                        "email": user.email,
                        'domain': domain,
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': protocol,
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        print(conf_settings.MAILGUN_KEY)
                        print(clean_mail)
                        rc = requests.post("https://api.mailgun.net/v3/sandbox1f42285ff9e446fa9e90d34287cd8fee.mailgun.org/messages",
                                           auth=("api", conf_settings.MAILGUN_KEY),
                                           data={"from": "Pur Beurre <webmaster@jm-hayons74.fr>",
                                                 "to": clean_mail,
                                                 "subject": subject,
                                                 "text": email,
                                                 })
                        print(rc)
                    except:
                        context['error'] = Translation.get_translation("Error sending mail", language)

                    context['success'] = Translation.get_translation(
                        'A message with reset password instructions has been sent to your inbox.',language)

            else:
                context['error'] = Translation.get_translation('An invalid email has been entered.', language)
        else:
            context['error'] = Translation.get_translation('An invalid email has been entered.', language)
            return redirect('user_app:reset_password', error=context['error'])

    else:
        form = PasswordResetForm()
    context['form'] = form
    return render(request, 'registration/reset_password.html', context=context)