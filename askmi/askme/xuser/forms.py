from django import forms

from .models import Post


class LogInForm(forms.ModelForm):

    class Meta:
        model = Xuser
        fields = ('username', 'password',)


class RegisterForm(forms.ModelForm)
	class Meta:
		model = Xuser
		fields = ('username','email','password',)
			


    