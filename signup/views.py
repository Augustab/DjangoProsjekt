'''filen til signup sitt view'''
# views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import RegisterForm
from main.models import Account


# Create your views here.
def signup(response):
    '''Signup sitt view'''
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(response, new_user)
            default_account = Account(name="default" + form.cleaned_data['username'], belop=0,
                                      interest=0, user=response.user)
            default_account.save()
            return redirect("/home")
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form": form})
