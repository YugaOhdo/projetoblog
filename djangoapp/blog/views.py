from typing import Any
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView 

PER_PAGE = 9
class Index(ListView):
    model = Post #nesse caso não precisa pois estamos passando uma queryset
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    ordering= '-pk',
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Home - '
        })
        return context
    
# def index(request):
#     posts = Post.objects.get_published()
    
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#         }
#     )

class Page(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    slug_field = 'slug'
    context_object_name = 'page'
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        context.update({
            'page_title': f'{page.title} - Página -'
        })
        return context

# def page(request, slug):
#     page = Page.objects.filter(is_published=True).filter(slug=slug).first()
#     if page is None:
#         raise Http404()
#     page_title = f'{page.title} - Página -'
#     return render(
#         request,
#         'blog/pages/page.html',
#         {
#             'page':page,
#             'page_title': page_title,
           
#         }
#     )

class Post(DetailView):
    model = Post
    template_name = 'blog/pages/post.html'
    slug_field = 'slug'
    context_object_name = 'post'
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context.update({
            'page_title': f'{post.title} - Post -'
        })
        return context

# def post(request, slug):
#     post = Post.objects.get_published().filter(slug=slug).first()
#     if post is None:
#         raise Http404()
#     page_title = f'{post.title} - Post - '
#     return render(
#         request,
#         'blog/pages/post.html',
#         {
#             'post': post,
#             'page_title': page_title,

#         }
#     )

class Created_by(Index):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context = {}
    
    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)
        return qs
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username
        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'
        page_title = user_full_name + ' posts - '
        ctx.update({
            'page_title' : page_title,
        })
        return ctx
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        author_id = self.kwargs.get('author_id')
        user = User.objects.filter(pk=author_id).first()
        if user is None:
            return redirect('blog:index')
        self._temp_context.update({
            'author_id': author_id,
            'user': user,
        })
        return super().get(request, *args, **kwargs)


# def created_by(request, author_id):
#     user = User.objects.filter(pk=author_id).first()
#     if user is None:
#         raise Http404()
#     posts = Post.objects.get_published().filter(created_by__pk=author_id)
#     user_full_name = user.username
#     if user.first_name:
#         user_full_name = f'{user.first_name} {user.last_name}'
#     page_title = user_full_name + ' posts - '
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )

class Category(Index):
    allow_empty = False #levanta 404 se estiver vazio
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': f'{self.object_list[0].category.name} - Categoria - '
        })
        return context

# def category(request, slug):
#     posts = Post.objects.get_published().filter(category__slug=slug)
#                                         # __ buscando de foreign key do post
#     if len(posts) == 0:
#         raise Http404()
        
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     page_title = f'{page_obj[0].category.name} - Categoria - '

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )

class Tag(Index):
    allow_empty = False #levanta 404 se estiver vazio
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            tag__slug=self.kwargs.get('slug')
        )
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': f'{self.object_list[0].tag.first().name} - Tag - '
        })
        return context

# def tag(request, slug):
#     posts = Post.objects.get_published().filter(tag__slug=slug)
#                                         # __ buscando de foreign key do post
    
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     page_title = f'{page_obj[0].tag.first().name} - Tag - '

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,

#         }
#     )

class Search(Index):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._search_value = ''
        
    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self._search_value = request.GET.get('search').strip()

        return super().setup(request, *args, **kwargs)
    
    def get_queryset(self) -> QuerySet[Any]:
        search_value = self._search_value
        return super().get_queryset().filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)   
        )[0:PER_PAGE]
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        search_value = self._search_value
        context.update({
            'page_title': f'{search_value[:30]} - Search -',
            'search_value': search_value,
        })
        return context
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)

# def search(request):
#     search_value = request.GET.get('search').strip()
#     posts = Post.objects.get_published().filter(
#         Q(title__icontains=search_value) |
#         Q(excerpt__icontains=search_value) |
#         Q(content__icontains=search_value)   
#     )[0:PER_PAGE]
#                                         # __ buscando de foreign key do post
#     page_title = f'{search_value[:30]} - Search -'

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': posts,
#             'search_value': search_value,
#              'page_title': page_title,
#         }
#     )