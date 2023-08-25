from .models import Post,Category, Tag
from django import forms
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)
    tags = forms.CharField(max_length=100, help_text="Enter comma-separated tags")
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = ['title','subtitle','cover_img','content','categories','tags']