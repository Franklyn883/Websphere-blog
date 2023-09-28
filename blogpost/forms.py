from .models import Post,Category
from django import forms
from ckeditor.widgets import CKEditorWidget



    
class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Post
        fields = ['title','subtitle','cover_img','content','categories']