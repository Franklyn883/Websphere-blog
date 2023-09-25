from .models import Post,Category, Tag
from django import forms
from taggit.forms import TagWidget
from ckeditor.widgets import CKEditorWidget

class PostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)
    content = forms.CharField(widget=CKEditorWidget())
    tags = forms.CharField(widget=TagWidget())
  
    class Meta:
        model = Post
        fields = ['title','subtitle','cover_img','content','categories','tags']