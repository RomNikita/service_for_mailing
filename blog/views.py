from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.forms import BlogCreateForm, BlogUpdateForm
from blog.models import Blog


class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogCreateForm
    success_url = reverse_lazy('blog:blog_list')
    template_name = 'blog_form.html'


class BlogListView(ListView):
    model = Blog
    template_name = 'blog_list.html'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_of_views += 1
        self.object.save()
        return self.object


class BlogUpdateView(UpdateView):
    model = Blog
    form_class = BlogUpdateForm
    template_name = 'blog_edit.html'

    def get_success_url(self):
        return reverse('blog:blog_detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
    template_name = 'blog_confirm_delete.html'

