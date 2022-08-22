from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        localizered_fields = ('text', 'group')
        help_text = {
            'text': 'Здесь вы можете написать/отредактировать сообщение',
            'group': 'Укажите группу, если вы хотите'
        }
