from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', cache_page(30)(MovieHome.as_view()), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', MovieCategory.as_view(), name='category'),
    path('add_comment/<str:post_slug>/', add_comment, name='add_comment'),
    path('blog/<int:blog_id>/edit/', edit_blog, name='edit_blog')
]