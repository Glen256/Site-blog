from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponse, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import AddPostForm, RegisterUserForm, LoginUserForm, ContactForm, CommentForm
from django.views.generic import ListView, DetailView, CreateView, FormView
# Create your views here.

from .models import *
from .utils import DataMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator


menu = [{'title': 'Про сайт', 'url_name': 'about'},
        {'title': 'Додати пост', 'url_name': 'add_page'},
        {'title': 'Зв\'язок з адміністратором', 'url_name': 'contact'},
        {'title': 'Увійти', 'url_name': 'login'}
        ]


class MovieHome(DataMixin, ListView):
    paginate_by = 3
    model = Movie
    template_name = 'movies/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Головна сторінка')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Movie.objects.filter(is_published=True).select_related('cat')


class MovieCategory(DataMixin, ListView):
    model = Movie
    template_name = 'movies/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Movie.objects.filter(cat__slug=self.kwargs['cat_slug'],
                                    is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категорія ' + str(context['posts'][0].cat),
                                      cat_selecred=context['posts'][0].cat_id)
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class ShowPost(DataMixin, DetailView):
    model = Movie
    template_name = 'movies/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        context = dict(list(context.items()) + list(c_def.items()))


        comments = Comments.objects.filter(new=context['post'])
        context['comments'] = comments


        context['comment_form'] = CommentForm()
        return context

def add_comment(request, post_slug):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = Movie.objects.get(slug=post_slug)
            comment.new_id = comment.post.id
            comment.save()
            return redirect('post', post_slug=post_slug)
    else:
        form = CommentForm()
    return render(request, 'post.html', {'form': form})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'movies/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Додавання посту')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'movies/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Реєстрація')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


def edit_blog(request, blog_id):
    blog = get_object_or_404(Movie, id=blog_id)

    if request.method == "POST":
        form = AddPostForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', blog_id=blog.id)
    else:
        form = AddPostForm(instance=blog)

    return render(request, 'edit_blog.html', {'form': form})


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'movies/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизація')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_success_url(self):
        return reverse_lazy('home')


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'movies/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Зв\'язок з адміністратором')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


def logout_user(request):
    logout(request)
    return redirect('login')




def about(request):
    contact_list = Movie.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,
                  'movies/about.html',
                  {'page_obj': page_obj,
                      'menu': menu,
                   'title': 'Сторінка про сайт',
                   })


def contact(request):
    return HttpResponse("Зв\'язок з адміністратором")


def login_view(request):
    return HttpResponse("Авторизація")


def show_category(request, cat_id):
    posts = Movie.objects.filter(cat_id=cat_id)
    cats = Category.objects.all()

    context = {'menu': menu,
               'cats': cats,
               'posts': posts,
               'cat_selected': cat_id}
    return render(request, 'movies/index.html', context=context)


def pageNotFound(request, exception):
    return HttpResponse("<h1>Сторінку не знайдено</h1>")


def archive(request, year):
    if (int(year) > 2023):
        return redirect('home', permanent=True)

    return HttpResponse(f"<h1>Архів по роках</h1>{year}<p>")
