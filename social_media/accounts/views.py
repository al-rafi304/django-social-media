from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


def login_account(request):
    # If form has been submitted
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Catching erros
        if user is not None:
            login(request, user)
            messages.success(request, f'You are now logged in as {request.user.username}')
            return redirect('home')
        else:
            # Login error message
            messages.error(request, ('Error loging in !!!'))
            return redirect('login')
    
    # Landing page
    else:
        return render(request, 'accounts/login.html', {})
    
def logout_account(request):
    logout(request)
    messages.warning(request, 'You were logged out')
    return redirect('home')