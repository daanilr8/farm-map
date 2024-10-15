"""
URL configuration for geospatial_project project.

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
from django.urls import path
from farm_management import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get-rover-data/', views.get_rover_data, name='get_data'),
    path('post-rover-data/',views.post_rover_data, name= 'post_data'),
    path('rover_map/',views.rover_map),
    path('farm_map/', views.farm_map),
]
