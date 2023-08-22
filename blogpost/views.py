from django.shortcuts import render
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Tag
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.
def get_tag_suggestions(request):
    input_value = request.GET.get('input', '')
    tags = Tag.objects.filter(name__icontains=input_value)[:10]
    suggestions = [{'name': tag.name} for tag in tags]
    return JsonResponse(suggestions, safe=False)

class BlogPostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'blogpost/post_create.html'  # Replace with your template path
    success_url = reverse_lazy('home')  # Replace with the appropriate URL

    def form_valid(self, form):
        form.instance.author = self.request.user
        categories = form.cleaned_data['categories']
        tags_input = form.cleaned_data['tags']
        tags_list = [tag.strip() for tag in tags_input.split(',')]
        
        for tag_name in tags_list:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            form.instance.tags.add(tag)

