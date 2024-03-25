from django.forms import CharField, TextInput, PasswordInput, Form


class LoginForm(Form):
    username = CharField(label='Username', widget=TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'placeholder': 'Username'
    }))
    password = CharField(label='Password', widget=PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'placeholder': 'Enter your password'
    }))


class RegisterForm(Form):
    first_name = CharField(label='First name', widget=TextInput(attrs={
        'class': 'form-control',
        'id': 'first_name',
        'placeholder': 'First name'
    }))
    last_name = CharField(label='Last name', widget=TextInput(attrs={
        'class': 'form-control',
        'id': 'last_name',
        'placeholder': 'Last name'
    }))
    email = CharField(label='Email', widget=TextInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'placeholder': 'Email'
    }))
    username = CharField(label='Username', widget=TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'placeholder': 'Username'
    }))
    password1 = CharField(label='Password', widget=PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'placeholder': 'Password1'
    }))
    confirmation = CharField(label='Confirm password', widget=PasswordInput(attrs={
        'class': 'form-control',
        'id': 'confirm',
        'placeholder': 'Confirm password'
    }))
