from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth import get_user_model
from .forms import CustomUserChangeForm, UserProfileUpdateForm
from django.contrib.auth.decorators import login_required

from django.contrib import messages

User = get_user_model()


def is_following(user, target_user):
    return target_user.profile in user.profile.following.all()


def profile_view(request, username=None):
    """Returns the profile of the request user, or the profile of the user, with the username in the url param."""
    
    is_following_user = None
    if username:
        profile = get_object_or_404(User, username=username).profile
        user = get_object_or_404(User,username=username)
        if request.user.is_authenticated:
            is_following_user = is_following(request.user,user)
        
    else:
        try:
        
            profile = request.user.profile
        except:
            Http404
         
    followers = profile.followers.all()
    followings = profile.following.all()  
    context = {"profile": profile,"followers":followers, "followings":followings, "is_following_user":is_following_user}

    return render(request, "accounts/user_profile.html", context)


@login_required
def profile_update(request):
    """Update the profile of the request user, using the custom user form and the profile form."""
    user_form = CustomUserChangeForm(instance=request.user)
    profile_form = UserProfileUpdateForm(instance=request.user.profile)
    if request.method == "POST":
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(
            request.POST, instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            profile = profile_form.save(commit=False)
            if "photo" in request.FILES:
                request.user.profile.photo = request.FILES.get("photo")
            user_form.save()
            profile.save()
            messages.success(request, "Your profile is updated successfully")
            return redirect("profile")
    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, "accounts/profile_update.html", context)

@login_required
def follow_user(request,username):
    """Adds a the request user to the following """
    user_to_follow = get_object_or_404(User,username=username)
    request.user.profile.following.add(user_to_follow.profile)
    messages.success(request, "Now following {}".format(user_to_follow.profile.name))
   
    context = {"post":user_to_follow.post.first(),"is_following_author":True}
    
    
    return render(request, "blogpost/snippets/_follow.html",context)

@login_required
def unfollow_user(request,username):
    """Removes the request user from following."""
    user_to_unfollow = get_object_or_404(User,username=username)
    request.user.profile.following.remove(user_to_unfollow.profile)
    messages.success(request, "unfollowed {}".format(user_to_unfollow.profile.name))
    
    context = {"post":user_to_unfollow.post.first(),"is_following_author":False}
    return render(request,"blogpost/snippets/_follow.html",context)
    
    
