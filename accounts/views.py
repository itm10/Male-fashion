from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, hashers, logout
from django.views import View
from django.contrib import messages

from .forms import LoginForm, RegisterForm

User = get_user_model()


class LoginView(View):
    template_name = 'login.html'
    contex = {}

    def get(self, request):
        form=LoginForm
        self.contex.update({'form': form})
        return render(request, self.template_name, self.contex)

    def post(self, request):
        form=LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Username or password is not valid!")
                return redirect('/accounts/login')


class RegisterView(View):
    template_name = 'register.html'
    contex = {}

    def get(self, request):
        form=RegisterForm
        self.contex.update({'form': form})
        return render(request, 'register.html', self.contex)

    def post(self, request):
        form=RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('confirmation')

            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.error(request, "This username already exists")
                    return redirect('/accounts/sign-up')
                if User.objects.filter(email=email).exists():
                    messages.error(request, "This email already exists")
                    return redirect('/accounts/sign-up')
                else:
                    user = User.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        username=username,
                        password=hashers.make_password(password2)
                    )
                    user.save()
                    return redirect('/accounts/login')
            else:
                messages.error(request, "Password are not the same")
                return redirect('/accounts/sign-up')


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('/')
