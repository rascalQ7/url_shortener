from django.urls import path
from website.views import home, dashboard, login_user, sign_up_user, logout_user

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', login_user, name='login'),
    path('signup/', sign_up_user, name='sign_up'),
    path('logout/', logout_user, name='logout'),
]
