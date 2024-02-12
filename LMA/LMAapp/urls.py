from .import views
from django.urls import path
from .views import signup ,home,add_to_bag


urlpatterns = [
    path('', views.index, name='index'),    
    path('add_to_bag/', add_to_bag, name='add_to_bag'),
    path('return_book', views.return_book, name='return_book'),
    path('home/display', views.home, name='home'),  
    path('accounts/login/', views.loginview, name='login'),
    path( 'logout', views.logoutview),  
    path('accounts/signup/', views.signup, name='signup'),
    path('mybag/display',views.mybag,name='mybag'),
    path('resfin',views.resfin,name='resfin')
]
