from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from .models import *


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

def register_account(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('edit-profile')
        else:
            messages.error(request, form.error_messages)
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {
        'form': form,
    })

@login_required
def edit_profile(request):
    if request.method == "POST":
        account = Account.objects.get(id = request.user.id)
        profile_pic = request.FILES.get('post-profile')
        cover_pic = request.FILES.get('post-cover')
        bio = request.POST['bio']
        address = request.POST['address']
        occupation = request.POST['occupation']
        relationshipStatus = request.POST['relationshipStatus']

        account.bio = bio
        account.address = address
        account.occupation = occupation

        if relationshipStatus == 'None':
            account.relationshipStatus = None
        else:
            account.relationshipStatus = relationshipStatus


        if profile_pic and profile_pic.name != account.profile_img.name:
            account.profile_img = profile_pic
        if cover_pic and cover_pic.name != account.cover_img.name:
            account.cover_img = cover_pic
        
        account.save()
        return redirect('profile', account_id = request.user.id)

    return render(request, 'accounts/editProfile.html', {})