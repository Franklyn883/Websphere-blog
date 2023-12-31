from .models import Post,Category,PostComment
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget


    
class PostForm(forms.ModelForm):
    
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['content'].required = False
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)
  
    class Meta:
        model = Post
        fields = ['title','subtitle','cover_img','content','categories']
        widgets = {
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            )
        }
        
class PostCommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'maxlength':1000,'class':'comment__textarea'}))
    class Meta:
        model = PostComment
        fields = ['comment', 'edited']
        widgets = {'edited': forms.HiddenInput()}
    