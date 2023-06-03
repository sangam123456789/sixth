from django.contrib import admin
from django.urls import path , include
from home import views

admin.site.site_header = "Welcome Mr. Administrator"
admin.site.site_title = "This is Admin zone"
admin.site.index_title = "Databases"
urlpatterns =[
    path('', views.hom , name = 'hom'),
    path('Order', views.ord , name = 'ord'),
    path('I-Veg', views.ive , name = 'ive'),
    path('I-Nve', views.inv , name = 'inv'),
    path('Chinese', views.chi , name = 'chi'),
    path('Special', views.spe , name = 'spe'),
    path('Contact', views.Contact , name = 'Contact'),
    path('signin', views.signin, name = 'signin'),
    path('signup', views.signup, name = 'signup'),
    path('signout', views.signout, name = 'signout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]
 