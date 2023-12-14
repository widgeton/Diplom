from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django import forms


class Register(forms.Form):
    name = forms.CharField(label='Имя', max_length=50)
    email = forms.EmailField(label='Почта')
    password = forms.CharField(label="Пароль", min_length=6, max_length=16, widget=forms.PasswordInput)
    repeat_password = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    attrs = {'style': "width: 300px", 'class': "form-control me-2"}
    name.widget.attrs.update(attrs)
    email.widget.attrs.update(attrs)
    password.widget.attrs.update(attrs)
    repeat_password.widget.attrs.update(attrs)

    def clean_repeat_password(self):
        rep_pass = self.cleaned_data['repeat_password']
        password = self.cleaned_data['password']
        if rep_pass != password:
            raise forms.ValidationError("Пароль повторен неверно!")
        return rep_pass


class Login(forms.Form):
    email = forms.EmailField(label="Почта")
    password = forms.CharField(label="Пароль", min_length=6, max_length=16, widget=forms.PasswordInput)

    attrs = {'style': "width: 300px", 'class': "form-control me-2"}
    email.widget.attrs.update(attrs)
    password.widget.attrs.update(attrs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data['email']
        password = cleaned_data['password']
        user = User.objects.filter(email=email).first()
        if user is None or not check_password(password, user.password):
            raise forms.ValidationError("Неверный email или пароль!")


class Create(forms.Form):
    word = forms.CharField(label="Слово или выражение", max_length=128)
    meaning = forms.CharField(label="Значение", widget=forms.Textarea)
    example = forms.CharField(label="Пример", widget=forms.Textarea, required=False)

    attrs = {'style': "width: 500px; margin: 8px;", 'class': "form-control me-2"}
    word.widget.attrs.update(attrs)
    meaning.widget.attrs.update(attrs)
    example.widget.attrs.update(attrs)


class ChangeName(forms.Form):
    name = forms.CharField(label='Новое имя', max_length=50)

    attrs = {'style': "width: 300px", 'class': "form-control me-2"}
    name.widget.attrs.update(attrs)


class ChangePassword(forms.Form):
    old_password = forms.CharField(label="Старый пароль", min_length=6, max_length=16, widget=forms.PasswordInput)
    password = forms.CharField(label="Новый пароль", min_length=6, max_length=16, widget=forms.PasswordInput)
    repeat_password = forms.CharField(label="Повторите новый пароль", widget=forms.PasswordInput)

    attrs = {'style': "width: 300px", 'class': "form-control me-2"}
    old_password.widget.attrs.update(attrs)
    password.widget.attrs.update(attrs)
    repeat_password.widget.attrs.update(attrs)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_repeat_password(self):
        rep_pass = self.cleaned_data['repeat_password']
        password = self.cleaned_data['password']
        if rep_pass != password:
            raise forms.ValidationError("Пароль повторен неверно!")
        return rep_pass

    def clean_old_password(self):
        user = User.objects.get(id=self.request.user.id)
        old_password = self.cleaned_data['old_password']
        if not check_password(old_password, user.password):
            raise forms.ValidationError("Неверный старый пароль!")
        return old_password
