"""mob_project URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from mob_app.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    ##########login & registration start
    url(r'^$',display_login),
    url(r'^show_register',show_register,name="show_register"),
    url(r'^register', register, name="register"),
    url(r'^display_login', display_login, name="display_login"),
    url(r'^check_login', check_login, name="check_login"),
    url(r'^logout',logout,name="logout"),
    ##########login & registration end

    ################Admin start
    url(r'^show_home_admin',show_home_admin,name="show_home_admin"),
    url(r'^view_users_admin',view_users_admin,name="view_users_admin"),
    url(r'^delete',delete,name="delete"),
    url(r'^display_add_mobile_admin',display_add_mobile_admin,name="display_add_mobile_admin"),
    url(r'^add_mobile',add_mobile,name="add_mobile"),
    url(r'^show_view_mobile_admin',show_view_mobile_admin,name="show_view_mobile_admin"),
    url(r'^mobile_delete',mobile_delete,name="mobile_delete"),
    ################Admin end

    ###############User start
    url(r'^show_home_user',show_home_user,name="show_home_user"),
    url(r'^display_find_my_mobile_user',display_find_my_mobile_user,name="display_find_my_mobile_user"),
    url(r'^find_mobile',find_mobile,name="find_mobile"),
    url(r'^display_similiar_phones_user',display_similiar_phones_user,name="display_similiar_phones_user"),
    url(r'^purchase_mobile',purchase_mobile,name="purchase_mobile"),
    url(r'^show_give_rating_user',show_give_rating_user,name="show_give_rating_user"),
    url(r'^display_mobile_list',display_mobile_list,name="display_mobile_list"),
    url(r'^add_rating',add_rating,name="add_rating"),
    url(r'^view_recommendations_user',view_recommendations_user,name="view_recommendations_user"),
    url(r'^get_recommendations',get_recommendations,name="get_recommendations"),
    ###############User end
]
