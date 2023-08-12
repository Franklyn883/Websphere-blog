from django.shortcuts import render
from .forms import CustomUsercreationForm

# Create your views here.
def registration(request):
    form = CustomUsercreationForm()
    context = {'form':form}
    return render(request, 'accounts/signup.html', context)