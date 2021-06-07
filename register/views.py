from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from store.models import Customer
from django.contrib.auth import logout

# Create your views here.

def register(response):
        if response.method == 'POST':
            form = RegisterForm(response.POST)
            if form.is_valid(): 
                #saving the registered user
                user = form.save()
                Customer.objects.create(
                    user = user,
                    name = user.username,
                    email = user.email
                )    
                username= form.cleaned_data.get('username') 
                messages.success(response, f'Your Account has been created! You can now log in')
                return redirect('/login')
        else:
            form = RegisterForm() #creates an empty form
        return render(response, 'register/register.html', {'form': form})
def logout_view(request):
    logout(request)


    