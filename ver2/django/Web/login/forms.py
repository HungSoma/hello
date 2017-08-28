from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

)
User = get_user_model()
class LoginForm(forms.Form):
    username = forms.CharField(label="Username", widget = forms.TextInput(attrs={'class':' form-control ', 'name': "username", 'placeholder':"Username", 'size': 80}))
    password = forms.CharField(label="Password", widget =forms.PasswordInput(attrs={'class':'form-control ', 'name':'password','placeholder':"PassWord", 'size': 80}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist.")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password !")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")

        return super(LoginForm, self).clean(*args, **kwargs)

class UserregisterForm(forms.ModelForm):
    username = forms.CharField( widget = forms.TextInput(attrs={'size': 30,'class': "form-control",'name': "username",'placeholder':"Username"}))
    email = forms.EmailField(label='Email address', widget = forms.TextInput(attrs={'size': 30,'class': "form-control",'placeholder':"Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'size':50,'class': "form-control",'placeholder':"Password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'size':50,'class': "form-control",'placeholder':"Confirm Password"}))
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'confirm_password'

        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        email_qs = User.objects.filter(email=email)
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if email_qs.exists():
            raise forms.ValidationError(
                " This email has already been registered"
            )
        if password != confirm_password:
            raise forms.ValidationError(
                " The password does not match"
            )
        return super(UserregisterForm, self).clean(*args,**kwargs)

class Password_reset(forms.Form):
    email = forms.EmailField(label='Email address', widget = forms.TextInput(attrs={'size': 30,'class': "form-control",'placeholder':"Email"}))



class Password_reset_change(forms.Form):
    newpassword_1 = forms.CharField(label = 'Password_1 ', widget = forms.PasswordInput(attrs={'size': 30, 'class': "form-control", 'placeholder':"New Password"}))
    confirm_password_1 = forms.CharField(label='Password_1 ', widget=forms.PasswordInput(attrs={'size': 30, 'class': "form-control", 'placeholder': "Confirm Password"}))

    def clean(self, *args, **kwargs):
        newpassword1 = self.cleaned_data.get("newpassword_1")
        confirmpassword1 = self.cleaned_data.get("confirm_password_1")
        if newpassword1 != confirmpassword1 :
            raise forms.ValidationError(" The Confirm Password didn't match. Pls try again ")
        return  super(Password_reset_change, self).clean(*args,**kwargs)







