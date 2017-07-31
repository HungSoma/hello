from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

)
User = get_user_model()
class UserloginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")


        if username or password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist.")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password !")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")

        return super(UserloginForm, self).clean(*args, **kwargs)

class UserregisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'

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








