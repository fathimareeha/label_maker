"""
URL configuration for shipping_label_maker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from label_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path('', views.LoginView.as_view(), name='root-login'),
    path('admin/', admin.site.urls),
    path('login/', views.LoginView.as_view(), name='login'),
    path('home',views.HomePageView.as_view(),name='home'),
    path('home_page',views.HomeView.as_view(),name='home_page'),
    path('label_create', views.LabelCreateView.as_view(), name='create-label'),
    path('label_list',views.LabelListView.as_view(),name='label_list'),
    path('update_label/<int:pk>',views.UpdateLabelStatusView.as_view(),name='update-label-status'),
   path('status_history/<int:pk>/', views.LabelStatusHistoryView.as_view(), name='label-status-history'),
    path('track',views.TrackingSearchView.as_view(),name='track-shipping-label'),
    path('track/search/', views.external_tracking_redirect, name='external-track-search'),
    path('delete/<int:pk>',views.LabelDeleteView.as_view(),name='delete'),
   

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
