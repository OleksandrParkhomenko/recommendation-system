from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, LoginForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Congratulations {username}! Your account is created!')
            return redirect('login')
    else:
        form = RegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)

