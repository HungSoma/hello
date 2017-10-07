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
from django.shortcuts import render, redirect, render_to_response
from .forms import LoginForm, UserregisterForm, Password_reset, Password_reset_change, UserForm, ProfileForm
from .models import UserProfile
from django.forms.models import inlineformset_factory

from django.template import  RequestContext
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
User =get_user_model()
# Create your views here.
def login_view(request):
    username = ' not logged in'
    form = LoginForm(request.POST or None)
    if request.session.has_key('username'):
        return redirect('/')
    else:
        if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    request.session['username'] =username
                    login(request, user)
                    return redirect("/")
                else:
                    return HttpResponse("Account deleted or disabled")
    context = {
        "form": form,
        "username": username,
    }
    response = render_to_response('login.html', context, context_instance=RequestContext(request))
    #response.set_cookie('last_connect', datetime.datetime.now())
    #response.set_cookie('username', username)
    return response

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
    try:
        del request.session['username']
    except:
        pass
    response = redirect("/")
    response.delete_cookie('user')
    return response
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
    #if 'username' in request.COOKIES   :
           # username =request.COOKIES['username']
            #last_connect = request.COOKIES['last_connect']
            #last_connect_time = datetime.datetime.strptime(last_connect[:-7],
            #    "%Y-%m-%d %H:%M:%S")
            #if (datetime.datetime.now() - last_connect_time).seconds < 10  :

           # return render(request, 'index.html', {"username":username})
            #else:
               # return redirect('/login/')

    if request.session.has_key('username'):

            username = request.session['username']
            return render(request, 'index.html', {"username": username})
    else:

            return redirect('/login/')
@login_required
def profile_user(request):
    pk = request.user.pk
    user = User.objects.get(pk = pk)
    user_form = UserForm(instance = user)
    Profile_InLine = inlineformset_factory(User, UserProfile, form = ProfileForm)
    formset = Profile_InLine(instance = user)
    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == 'POST':
            user_form = UserForm(request.POST, request.FILES, instance = user)
            formset = Profile_InLine( request.POST, request.FILES, instance = user)

            if user_form.is_valid() and formset.is_valid():
                created_user = user_form.save(commit = False)
                created_user.save()
                formset.save()
                return redirect('/profile/')
        return  render(request, "profile.html", {
            "noodle": pk,
            "first_form": user_form,
            "formset": formset,
        })
    else:
        raise  PermissionError
def profile(request):
    user_profile_data = UserProfile.objects.filter(user =request.user)
    return render(request, 'profileNew.html', {'profile_data':user_profile_data})
