from django.shortcuts import render
from django.http import Http404
from django.views.generic import (
    ListView, DetailView, CreateView, DeleteView, UpdateView
)
from .models import Post, Category, Location
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
# Create your views here.


class Index(ListView):
    model = Post
    paginate_by = 5
    queryset = Post.objects.select_related(
        'location', 'category'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )
    template_name = 'blog/index.html'


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_queryset(self):
        return super().get_queryset().select_related('location', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk', None)
        post = get_object_or_404(
            self.get_queryset(),
            pk=pk,
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        )
        context['post'] = post
        return context


class CategoryPosts(ListView):
    model = Category
    template_name = 'blog/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug', None)
        category = get_object_or_404(
            Category,
            slug=category_slug,
            is_published=True
        )
        context['category'] = category
        context['post_list'] = Post.objects.select_related(
            'category', 'location'
        ).filter(
            category=category.pk,
            is_published=True,
            pub_date__lte=timezone.now())
        return context
