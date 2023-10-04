from django.shortcuts import render, redirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth import get_user_model
from .forms import CustomUserChangeForm,UserProfileUpdateForm
from .models import UserProfile


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = CustomUserChangeForm
    template_name = 'profile_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = UserProfileUpdateForm(instance=self.object)
        return context

    def form_valid(self, form):
        profile_form = UserProfileUpdateForm(
            self.request.POST,
            instance=self.object
        )
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            return self.form_valid(form)
        return self.form_invalid(form)