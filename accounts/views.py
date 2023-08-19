from django.shortcuts import render, redirect
from .forms import CustomUsercreationForm
from django.contrib import  messages

# Create your views here.
def registration(request):
    form = CustomUsercreationForm()
    context = {'form':form}
    print(request)
    if request.method == 'POST':
        form = CustomUsercreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account was created successfully")
            return redirect('login')
       
    return render(request, 'accounts/signup.html', context)

def login_page(request):
    return render(request, 'accounts/login.html', {})