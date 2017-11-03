"""askme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include 
from django.contrib import admin
from home.views import HomeView, detailView
from post.views import PostView
from home.views import UserFormView,LogInFormView,profileView,logout_view
from django.contrib.auth import views as auth_views
from django.conf.urls import url


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/$',UserFormView.as_view(),name="UserFormView"),
    url(r'^profile/$',view = profileView, name = "ProfileView"),
    #url(r'^Notifications/$',view = notificationView, name = "Notifications"),
    url(r'^$',view = HomeView, name = "HomeView"),
    url(r'^ask/$',view = PostView, name = "PostView"),
    url(r'^details/(?P<post_id>[0-9]+)/$',view = detailView, name = "detailView"),
    url(r'^login/$',auth_views.login,name ='login'),
    url(r'^logout/$',view = logout_view,name = 'logout_view'),
    #url(r'^logout/$',auth_views.logout,{'next_page':'home:login'},name = 'logout'),
    url(r'^accounts/profile/$',profileView, name = 'profileView'),
]
