import random

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages
from django.views.generic import TemplateView, ListView

from .forms import AccountForm, ConnexionForm, SaveForm
from website.models import Category, Product

from website.scripts import main as m

def result(request):
    query = request.GET.get('query')
    products = Product.objects.filter(name_prod__icontains=query)
    if not products:
        messages.add_message(request, messages.WARNING, "Le produit demandé n'est pas dans notre base de données. Veuillez recommencer votre recherche.")
    else:
        number = random.randint(0, len(products)-1)
        choice = products[number]
        dico = choice.categories.all()
        substitutes_list = Product.objects.filter(categories__name_cat__exact=dico[0], grade__in='ab').order_by('name_prod')
        if not substitutes_list:
            messages.add_message(request, messages.WARNING, "Nous n'avons pas de produit de meilleure qualité à vous proposer.")
        else:
            paginator = Paginator(substitutes_list, 6)
            page = request.GET.get('page')
            substitutes = paginator.get_page(page)
    if request.method == 'POST':
        form = SaveForm(request.POST or None)
        if form.is_valid():
            article_id = form.cleaned_data['article_id']
            user_id = request.user.id
            product = Product.objects.get(id=article_id)
            product.fav.add(user_id)
            messages.add_message(request, messages.SUCCESS, 'Le produit a bien été sauvegardé!')

    return render(request, 'website/result.html', locals())

def my_products(request, page=1):

    if not request.user.is_authenticated:
        return redirect('connexion')
    else:
        user_id = request.user.id
        my_products_list = Product.objects.filter(fav=user_id).order_by('name_prod')
        paginator = Paginator(my_products_list, 6)
        try:
            my_products = paginator.page(page)
        except EmptyPage:
            my_products = paginator.page(paginator.num_pages)
        
    return render(request, 'website/my_products.html', locals())

def search(request, page=1):

    query = request.GET.get('query')
    products_list = Product.objects.filter(name_prod__icontains=query).order_by('name_prod')
    if not products_list:
        messages.add_message(request, messages.WARNING, "Le produit demandé n'est pas dans notre base de données. Veuillez recommencer votre recherche.")
    else:
        paginator = Paginator(products_list, 6)
        page = request.GET.get('page')
        products = paginator.get_page(page)
   
    return render(request, 'website/search.html', locals())

def product_page(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    return render(request, 'website/product_page.html', {'product':product})

def account_create(request):

    if not request.user.is_authenticated:        
        form = AccountForm(request.POST or None)
        if form.is_valid(): 
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            mail = form.cleaned_data['mail']
            password = form.cleaned_data['password']
            try:
                username_test = User.objects.get(username=username)
                messages.add_message(request, messages.WARNING, "Un compte existe déjà avec ce nom d'utilisateur. Merci d'en choisir un autre.")
            except User.DoesNotExist:
                user = User.objects.create_user(username, mail, password)
                user.first_name, user.last_name = first_name, last_name
                user.save()
                login(request, user)
                return redirect('account')                
    else:
        return redirect('account')

    return render(request, 'website/account_create.html', locals())

def connexion(request):
    error = False

    if not request.user.is_authenticated:
        form = ConnexionForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('account')
            else:
                error = True
    else:
        return redirect('account')

    return render(request, 'website/connect.html', locals())

def deconnexion(request):
    logout(request)
    return redirect(reverse(connexion))

def account(request):

    if not request.user.is_authenticated:
        return redirect('connexion')
    if request.method == 'POST':
        MAIN = m.Main()
        MAIN.request("chocolat")
        MAIN.request("viande")
        MAIN.request("yaourt")
        MAIN.request("soda")
        MAIN.request("pates-a-tartiner")

    return render(request, 'website/account.html', locals())
