"""
URL configuration for tasks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from Tasks import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('',views.task_list, name = ''),
    path('Tasks/<int:id>',views.Task_detail),
    path('add_task/', views.add_task, name = 'add_task'),
    path('check_task/<int:id>/', views.check_task, name='check_task'),
    path('undo_task/', views.undo_task, name='undo_task'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('api/tasks/', views.Task_list, name='api_task_list'),
    path('api/tasks/<int:id>/', views.Task_detail, name='api_task_detail'),

    # HTML Template Rendering
  

]

format_suffix_patterns(urlpatterns)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)