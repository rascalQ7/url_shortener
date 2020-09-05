from django.contrib import admin
from django.urls import path
from website.views import home, dashboard, login_user, sign_up_user, logout_user
from tiny_urls.views import external_redirection

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', login_user, name='login'),
    path('signup/', sign_up_user, name='sign_up'),
    path('logout/', logout_user, name='logout'),
    path('<str:tiny_url>', external_redirection),
]
