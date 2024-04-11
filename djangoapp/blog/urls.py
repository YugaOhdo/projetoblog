
from django.contrib import admin
from django.urls import path
from blog.views import Index, Page, Post, Created_by, Category, Tag, Search

app_name = 'blog'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('post/<slug:slug>', Post.as_view(), name='post'),
    path('page/<slug:slug>', Page.as_view(), name='page'),
    path('created_by/<int:author_id>/', Created_by.as_view(), name='created_by'),
    path('category/<slug:slug>', Category.as_view(), name='category'),
    path('tag/<slug:slug>', Tag.as_view(), name='tag'),
    path('search/', Search.as_view(), name='search'),


]
