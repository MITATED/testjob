from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.db.models import Count
from django.contrib import auth
from django.shortcuts import redirect
from django.views.generic import (
    ListView,
    TemplateView,
    DetailView,
    UpdateView,
    CreateView
)


class ListUsers(LoginRequiredMixin, TemplateView):
    model = User
    template_name = 'users.html'

    def get_context_data(self):
        context = super(ListUsers, self).get_context_data()
        context["users_and_posts"] = []  # Содержит словарь с авторами и записями каждого автора
        user_objects = User.objects.annotate(count=Count('post')).all()  # Все пользователи с количеством записей
        for user_object in user_objects:
            # Выбираем определенное кол-во последних записей пользователя
            if user_object == self.request.user:  # Выводить неопубликованые записи только текущего пользователя
                posts = Post.objects.order_by("-post_date_created").filter(post_author=user_object.id)[:3]
            else:
                posts = Post.objects.order_by("-post_date_created").filter(post_author=user_object.id,
                                                                           post_is_released=True)[:3]
            context["users_and_posts"] += [{"posts": posts, "user_object": user_object}]
        return context


class ListPostsFromUser(LoginRequiredMixin, ListView):
    template_name = 'user.html'
    context_object_name = "posts_one_user"
    paginate_by = 3

    def get_queryset(self):
        # Выводить неопубликованые записи только текущего пользователя
        if self.request.user.id == int(self.kwargs['pk']):
            posts_one_user = Post.objects.order_by("-post_date_created").filter(post_author=self.kwargs['pk'])
        else:
            posts_one_user = Post.objects.order_by("-post_date_created").filter(post_author=self.kwargs['pk'],
                                                                                post_is_released=True)
        return posts_one_user

    def get_context_data(self, **kwargs):
        context = super(ListPostsFromUser, self).get_context_data(**kwargs)
        context["user_object"] = User.objects.get(id=self.kwargs["pk"])
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    template_name = 'post.html'
    model = Post
    context_object_name = "post"

    def get(self, *args, **kwargs):
        get = super(PostDetailView, self).get(*args, **kwargs)
        # Если запись неопубликована не текущего пользователя то запрещаем просматривать
        if (not self.object.post_is_released) and (self.object.post_author != auth.get_user(self.request)):
            return redirect('blog:users_posts')
        return get

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context["is_post_this_user"] = auth.get_user(self.request) == self.object.post_author
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['post_name', 'post_text', 'post_is_released']
    template_name = 'update.html'

    def get(self, *args, **kwargs):
        get = super(PostUpdateView, self).get(*args, **kwargs)
        # Редиректим если нет доступа
        if self.object.post_author != auth.get_user(self.request):
            return redirect('blog:users_posts')
        return get


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['post_name', 'post_text', 'post_is_released']
    template_name = 'update.html'

    def form_valid(self, form):
        form.instance.post_author = self.request.user
        return super(PostCreateView, self).form_valid(form)
