from django.urls import path
from django.views.decorators.cache import cache_page

from blog.views import BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView

app_name = 'blog'

urlpatterns = [path('create/', BlogCreateView.as_view(), name='blog_create'),
               path('', cache_page(60)(BlogListView.as_view()), name='blog_list'),
               path('<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
               path('edit/<int:pk>/', BlogUpdateView.as_view(), name='blog_edit'),
               path('delete/<int:pk>', BlogDeleteView.as_view(), name='blog_delete')
               ]