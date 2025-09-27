from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm


# Create your views here.

def register_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() # creates the User with username, email, hashed password
            messages.success(request, "Account created. You can now log in.")
            return redirect('login')
        else:
            print(form.errors) # inspect errors in terminal
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {"form": form})