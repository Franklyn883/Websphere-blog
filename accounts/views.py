from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import UpdateView
from django.contrib.auth import get_user_model
from .forms import CustomUserChangeForm,UserProfileUpdateForm
from .models import Profile
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django. contrib import messages 




@login_required
def profile_update(request):
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='user_profile',pk=request.user.pk)
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/profile_update.html', {'user_form': user_form, 'profile_form': profile_form})


    
class UserProfileView(View):
    template_name = 'accounts/user_profile.html'

    def get(self, request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)
        return render(request, self.template_name, {'user': user})