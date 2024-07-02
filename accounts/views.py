from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth import get_user_model
from .forms import CustomUserChangeForm, UserProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from blogpost.models import Post

User = get_user_model()


@login_required
def profile_view(request, username=None):
    """Returns the profile of the request user, or the profile of the user, with the username in the url param."""
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            Http404
    context = {"profile": profile}

    return render(request, "accounts/user_profile.html", context)


@login_required
def profile_update(request):
    """Update the profile of the request user, using the custom user form and the profile form."""
    user_form = CustomUserChangeForm(instance=request.user)
    profile_form = UserProfileUpdateForm(instance=request.user.profile)
    if request.method == "POST":
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile is updated successfully")
            return redirect("profile")
    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, "accounts/profile_update.html", context)
