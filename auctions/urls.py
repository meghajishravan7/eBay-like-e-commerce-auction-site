from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create', views.createlisting, name='create'),
    path('category_display', views.category_display, name='category_form'),
    path('listing/<int:id>', views.listing, name='listing'),
    path('remove/<int:id>', views.removewatchlist, name='remove'),
    path('add/<int:id>', views.addwatchlist, name='add'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('addbid/<int:id>', views.addbid, name='addbid'),
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),
    path('close/<int:id>', views.close, name='close')
]
