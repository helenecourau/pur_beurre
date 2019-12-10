from django.conf.urls import url
from django.views.generic import TemplateView
from django.urls import path
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='website/home.html'),
         name="home"),
    url('accueil',  TemplateView.as_view(template_name='website/home.html'),
        name="home"),
    url('mentions-legales',
        TemplateView.as_view(template_name='website/legal.html')),
    path('creer-compte', views.account_create, name="account_create"),
    path('connexion', views.connexion, name="connexion"),
    path('deconnexion', views.deconnexion, name='deconnexion'),
    path('mon-compte', views.account, name='account'),
    path('resultats/', views.result, name='result'),
    path('mes-aliments/', views.my_products, name='my_products'),
    path('recherche/', views.search, name='search'),
    path('produit/<int:id>-<slug:slug>',
         views.product_page, name='product_page'),
    url(r'^resultats/(?P<page>\d+)$', views.result, name='result'),
    url(r'^recherche/(?P<page>\d+)$', views.search, name='search'),
    url(r'^mes-aliments/(?P<page>\d+)$',
        views.my_products, name='my_products'),
]
