from django import forms

class SignUpForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=20)
    last_name = forms.CharField(label='Last name', max_length=20)
    username = forms.CharField(label='Username', max_length=20)
    email = forms.EmailField(label='Email', max_length=200)
    password = forms.CharField(label='Password', widget = forms.PasswordInput())
    computing_id = forms.CharField(label='Computing ID', max_length=10)
    phone_number = forms.CharField(label='Phone number', max_length=20)
    bio = forms.CharField(max_length=500, widget=forms.Textarea)
    #profile_image = forms.ImageField(default='default.png', upload_to='profile_pics')

    
class LogInForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password', widget = forms.PasswordInput())
