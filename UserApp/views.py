from django.shortcuts import render, redirect
from .forms import registerUserForm
from django.contrib.auth import logout

def register(req):
    if req.method == "POST":
        form = registerUserForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = registerUserForm()
    
    return render(req, 'register.html', {"form": form})

def logout_view(req):
    logout(req)
    return redirect("login")