from django import forms
from django.utils import timezone

from .models import Post, Comment, User


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        edit = kwargs.pop('edit', False)

        super(PostForm, self).__init__(*args, **kwargs)

        if edit and self.instance and self.instance.pub_date < timezone.now():
            self.fields['pub_date'].widget = forms.HiddenInput()

    class Meta:
        model = Post
        exclude = ('author', 'is_published')
        widgets = {
            'pub_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date',
                       'min': timezone.now().date().isoformat()}
            )
        }
        localized_fields = ('pub_date',)

    def save(self, commit=True):
        comment = super(PostForm, self).save(commit=False)
        if self.author is not None:
            comment.author = self.author
        if commit:
            comment.save()
        return comment


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.post = kwargs.pop('post', None)
        self.author = kwargs.pop('author', None)

        super(CommentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Comment
        fields = ('text',)

    def save(self, commit=True):
        comment: Comment = super(CommentForm, self).save(commit=False)
        if self.post is not None:
            comment.post = self.post
        if self.author is not None:
            comment.author = self.author
        if commit:
            comment.save()
        return comment


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
