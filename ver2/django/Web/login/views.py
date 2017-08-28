from django.http import  HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import  login_required
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

)
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from .forms import LoginForm, UserregisterForm, Password_reset, Password_reset_change

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
User =get_user_model()
# Create your views here.
def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return HttpResponse("Account deleted or disabled")

    return render(request, 'login.html', {"form":form})

def register(request):
    form = UserregisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit= False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user= authenticate(username=user.username, password = password)
        login(request, new_user)
        return redirect("/login")
    return render(request, 'register.html', {"form":form})

def logout_view(request):
    logout(request)
    return redirect ("/")
def password_reset(request):
    form = Password_reset(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        #send_mail
        get_user = User._default_manager.filter(email__iexact = email)
        if get_user.exists() :
            for user in get_user :
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
                subject = " Password reset "
                from_email = settings.EMAIL_HOST_USER
                c = {
                    'email': user.email,
                    'domain': domain,
                    'site_name': site_name,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'https' if False else 'http',
                }
                html_mail = render_to_string('registration/password_reset_email.html', c)
                send_mail(subject, html_mail, from_email,[email] )
                return redirect("/password_reset/done")
        else:
            messages.error(request, "Email doesn't exist. Make sure your email has been registered.")

    return render(request, 'registration/password_reset.html', {"form":form})
def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')
def password_reset_change(request, uidb64 = None, token = None):
    form = Password_reset_change(request.POST or None)
    assert uidb64 is not None and token is not None
    try :
        uid = urlsafe_base64_decode(uidb64)
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not  None and default_token_generator.check_token(user, token):
        validlink = True
        if form.is_valid():
            new_password = form.cleaned_data.get('confirm_password_1')
            user.set_password(new_password)
            user.save()
            return redirect('/reset_password/confirm/done')
    else:
        validlink = False
    context = {
        'form': form,
        'validlink': validlink,
    }

    return  render(request, 'registration/password_reset_confirm.html', context)
def password_reset_change_done(request):
    return render(request, 'registration/password_reset_confirm_done.html')

@login_required(login_url='/login/')
def home(request):
    return render(request, 'index.html', {})