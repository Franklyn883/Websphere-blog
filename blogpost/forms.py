from .models import Post,Category
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget


    
class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # it is required to set it False,
        # otherwise it will throw error in console
        self.fields["content"].required = False
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()
        self.save_m2m()
        return instance
    class Meta:
        model = Post
        fields = ['title','subtitle','cover_img','content','categories','tags']
        widgets = {
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            )
        }