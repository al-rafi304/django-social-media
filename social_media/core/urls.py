from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name ='home'),
    path('profile/<int:account_id>', views.profilePage, name='profile'),
    path('post', views.post, name='post'),
    path('<int:post_id>/sharePost', views.sharePost, name='share-post'),
    path('<int:post_id>/comment', views.comment, name='comment'),
    path('<int:post_id>/like', views.like, name='like'),
    path('<int:comment_id>/comment-like', views.commentLike, name='comment-like'),
]