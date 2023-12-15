from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import login, logout
from . import models
from . import forms


def index(request):
    cards = models.Card.objects.all()[:10]
    return render(request, 'siteapp/index.html', context={'cards': cards})


def about(request):
    return HttpResponse("About us")


def register(request):
    if request.method == 'POST':
        form = forms.Register(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=name, email=email, password=password)
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = forms.Register()
    context = {'form': form, 'button': 'Зарегистрироваться'}
    return render(request, 'siteapp/form.html', context)


def login_view(request):
    if request.method == 'POST':
        form = forms.Login(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = forms.Login()

    context = {'form': form, 'login_page': True, 'button': 'Войти'}
    return render(request, 'siteapp/form.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')


def create(request):
    if request.method == 'POST':
        form = forms.Create(request.POST)
        if form.is_valid():
            word = form.cleaned_data['word']
            meaning = form.cleaned_data['meaning']
            example = form.cleaned_data['example']
            card = models.Card(word=word, meaning=meaning, example=example, user=request.user)
            card.save()
            return redirect('index')
    else:
        form = forms.Create()

    context = {'form': form}
    return render(request, 'siteapp/create.html', context)


def like(request, card_id):
    card = models.Card.objects.filter(id=card_id).first()
    if request.user.is_authenticated:
        mark = models.Mark.objects.filter(user=request.user, card=card).first()
        if mark is None:
            mark = models.Mark(user=request.user, card=card, mark=models.Mark.LIKE)
            card.likes += 1
        elif mark.mark == mark.DISLIKE:
            card.dislikes -= 1
            mark.mark = mark.LIKE
            card.likes += 1
        card.save()
        mark.save()

    return redirect(request.META['HTTP_REFERER'])


def dislike(request, card_id):
    card = models.Card.objects.filter(id=card_id).first()
    if request.user.is_authenticated:
        mark = models.Mark.objects.filter(user=request.user, card=card).first()
        if mark is None:
            mark = models.Mark(user=request.user, card=card, mark=models.Mark.DISLIKE)
            card.dislikes += 1
        elif mark.mark == mark.LIKE:
            card.likes -= 1
            mark.mark = mark.DISLIKE
            card.dislikes += 1
        card.save()
        mark.save()

    return redirect(request.META['HTTP_REFERER'])


def setting(request):
    chn = forms.ChangeName()
    chp = forms.ChangePassword(request)
    if request.method == 'POST':
        if 'name' in request.POST:
            chn = forms.ChangeName(request.POST)
            if chn.is_valid():
                user = User.objects.get(id=request.user.id)
                user.username = chn.cleaned_data['name']
                user.save(update_fields=["username"])
                return redirect('index')
        elif 'password' in request.POST:
            chp = forms.ChangePassword(request, request.POST)
            if chp.is_valid():
                logout(request)
                user = User.objects.get(id=request.user.id)
                password = chp.cleaned_data['password']
                user.password = make_password(password)
                user.save(update_fields=["password"])
                login(request, user)
                return redirect('index')

    context = {'forms': (chn, chp)}
    return render(request, 'siteapp/setting.html', context)


def search(request):
    query = request.POST.get('search')
    if query != -1:
        cards = models.Card.objects.filter(word__contains=query).all()
        return render(request, 'siteapp/index.html', context={'cards': cards})
    return redirect(request.META['HTTP_REFERER'])
