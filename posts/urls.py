from django.contrib import admin
from django.urls import path
from . import views

app_name='posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_id>/', views.detail, name='detail'),
    path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),
    path('<int:post_id>/edit/', views.edit, name='edit'),
    path('<int:post_id>/update/', views.update, name='update'),
    path('<int:post_id>/delete/', views.delete, name='delete'),
    path('<int:post_id>/comment_create/', views.comment_create, name='comment_create'),
    path('<int:post_id>/tagforpost/', views.tagforpost, name='tagforpost'),
    path('<int:comment_id>/comment_edit/', views.comment_edit, name='comment_edit'),
    path('<int:comment_id>/comment_update/', views.comment_update, name='comment_update'),
    path('<int:comment_id>/comment_delete/', views.comment_delete, name='comment_delete'),
    path('<int:tag_id>/tag_filter/', views.tag_filter, name='tag_filter'),
    path('<int:tag_id>/filter_page/', views.filter_page, name="filter_page"),
    path('<int:comment_id>/tagforcomment/', views.tagforcomment, name='tagforcomment'),
    path('<int:post_id>/like', views.like, name='like'),
    path('<int:user_id>/profile_page/', views.profile_page, name='profile_page'),
    path('<int:post_id>/post_to_user/', views.post_to_user, name='post_to_user'),
]
