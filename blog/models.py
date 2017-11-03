from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse


class Post(models.Model):
    post_name = models.CharField(max_length=256, verbose_name="Название поста")
    post_text = RichTextField(verbose_name="Текст")
    post_date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    post_date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата последней модификации")
    post_is_released = models.BooleanField(default=True, verbose_name="Статус публичности")
    post_author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор поста")

    def __str__(self):
        return "(%s) %s" % (self.post_author, self.post_name)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
