from django import forms


class SignUpForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=20)
    last_name = forms.CharField(label='Last name', max_length=20)
    username = forms.CharField(label='Username', max_length=20)
    email = forms.EmailField(label='Email', max_length=200)
    password = forms.CharField(label='Password', widget = forms.PasswordInput())
    computing_id = forms.CharField(label='Computing ID', max_length=10)
    phone_number = forms.CharField(label='Phone number', max_length=20)
    bio = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'cols': 10, 'rows': 4}), required=False)
    #profile_image = forms.ImageField(default='default.png', upload_to='profile_pics')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

    
class LogInForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password', widget = forms.PasswordInput())


class CreatePostForm(forms.ModelForm):
    title = forms.CharField(max_length=100, label="Title of your post")
    content = forms.CharField(max_length=3000, label="Describe your post briefly", widget=forms.Textarea(attrs={'cols': 10, 'rows': 4}))
    price = forms.FloatField(min_value=0, label="How much do you want to sell for a single swipe?")
    remaining_nums = forms.IntegerField(min_value=0, label="How many swipes do you plan to sell?")
    pickup_address = forms.CharField(max_length=300, label="Where do you plan to meet the buyer?")
