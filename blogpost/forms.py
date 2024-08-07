from .models import Post,Category,PostComment, Reply
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from django.forms import ModelForm
    
class PostForm(ModelForm):
    
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['content'].required = False
    class Meta:
        model = Post
        fields = ['title','subtitle','cover_img','content','categories']
        widgets = {
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            ),
            "categories":forms.CheckboxSelectMultiple(),
        }
        
class PostCommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'maxlength':1000,'class':'comment__textarea'}))
    class Meta:
        model = PostComment
        fields = ['comment', 'edited']
        widgets = {'edited': forms.HiddenInput()}
    
class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ["body","edited"]
        labels ={
            "body":""
        }
        widgets = {
            "edited": forms.HiddenInput(),
            "body": forms.Textarea(attrs={"placeholder":"Enter reply","class":"comment__reply"})
        }