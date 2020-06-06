from django.urls import path
from . import views
app_name = 'homepage'
urlpatterns = [
    # ex:/homepage/
    path('', views.homepages, name='homepages'),
    # ex:/homepage/login/
    path('login/', views.login, name='login'),
    # ex:/homepage/register/
    path('register/', views.register, name='register'),
    # ex:/homepage/logout/
    path('logout/', views.logout, name='logout'),
    # ex:/homepage/1000/
    path('people<int:user_id>/', views.index, name='index'),
    path('rating/', views.rating, name='rating'),
    path('search/', views.search, name='search')

]
