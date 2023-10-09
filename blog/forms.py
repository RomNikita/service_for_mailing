from django import forms

from blog.models import Blog


class BlogCreateForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = '__all__'


class BlogUpdateForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = '__all__'