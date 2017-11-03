from django.conf.urls import url
from .views import *

app_name = 'blog'

urlpatterns = [
    url(r'users/$', ListUsers.as_view(), name="users_posts"),
    url(r'users/(?P<pk>\d+)/$', ListPostsFromUser.as_view(), name="user_posts"),
    url(r'(?P<pk>\d+)/$', PostDetailView.as_view(), name="post_detail"),
    url(r'(?P<pk>\d+)/update/$', PostUpdateView.as_view(), name="post_update"),
    url(r'create/$', PostCreateView.as_view(), name="post_create"),
]


# /blog/users/ — список всех пользователей
# /blog/users/2/ — список записей пользователя с ID 2
# /blog/2/ — Страница Post с ID 2
# /blog/2/update/ — Страница редактирования Post с ID 2
# /blog/create/ — Страница добавления поста
