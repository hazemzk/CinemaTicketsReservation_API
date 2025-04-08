"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from tickets import views 
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('guests', views.viewsets_guest)
router.register('movie', views.viewsets_movie)
router.register('reservations', views.viewsets_reservations)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1
    path("django/jsonresponmodel/", views.no_rest_no_model,name="jsonresponmodel"),
    
    # 2 
    path("django/jsonresponsfrommodel/", views.no_rest_form_model,name="jsonresponmodel"),

    #3 GET  POST from rest fremework func based views @api_view
    path("rest/fbv/", views.FBV_List),
    
    #3.2 GET  POST from rest fremework func based views @api_view
    path("rest/fbv/<int:pk>/", views.FBV_pk),
    
    
    ##4 GET  POST from rest fremework CBV       APIVeiw
    path('rest/cbv/', views.CBV_list.as_view()),
        ##4 GET  PUT DELETE from rest fremework CBV       APIVeiw
    path('rest/cbv/<int:pk>', views.CBV_pk.as_view()),
    
    ##5 GET  POST from rest fremework CBV  mixins
    path('rest/mixins/', views.mixins_list.as_view()),
        ##5 GET  PUT DELETE from rest fremework CBV mixins
    path('rest/mixins/<int:pk>', views.mixins_pk.as_view()),
    ##6 GET  POST from rest fremework CBV  generics
    path('rest/generics/', views.generics_list.as_view()),
        ##6 GET  PUT DELETE from rest fremework CBV generics
    path('rest/generics/<int:pk>', views.generics_pk.as_view()),
    
    ##7 GET  PUT DELETE from rest fremework viewsets
    path('rest/viewsets/', include(router.urls)),
    
    ## 8 FIND MOVIe 
    path('fbv/findmovie/', views.find_movie),
    
    ## 9 create reservation
    path('fbv/reservation/', views.newservation),
    
    #10 rest auth url
    path('api-auth/', include('rest_framework.urls')),
    
    # 11 token auth url
    path('api-token-auth', obtain_auth_token),
    
    #12 post pk 
    path('post/generics/', views.Post_list.as_view()),
    path('post/generics/<int:pk>', views.Post_pk.as_view()),
]
