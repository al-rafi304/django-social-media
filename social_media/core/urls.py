from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ='home'),
    path('post', views.post, name='post'),
    path('<int:post_id>/comment', views.comment, name='comment'),
    
]