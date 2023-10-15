from django.forms import ModelForm, BooleanField  # Импортируем true-false поле
from .models import Post
from django import forms
from django.utils.safestring import mark_safe


# Создаём модельную форму
class PostForm(ModelForm):
    check_box = BooleanField(label='Согласен с правилами сайта', required=False)  # добавляем галочку или же true-false поле

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['check_box'].widget = forms.CheckboxInput(attrs={'type': 'checkbox'})
        self.fields['check_box'].label = mark_safe('Согласен с <a href="http://127.0.0.1:8000/news/rules.html">правилами сайта</a>')

    # в класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля.
    # Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['title', 'text', 'postCategory', 'author']