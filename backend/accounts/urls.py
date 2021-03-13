from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),   
    # path('profile/<int:user_pk>/', csrf_exempt(views.ProfileView.as_view()), name='profile'),
    path('profile/', views.getInfo, name='getInfo'),
    path('checkemail/', views.check_email, name='check_email'),

]