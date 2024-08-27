from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        'Group',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    def __str__(self):
        return self.text


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, verbose_name='URL')
    description = models.TextField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             related_name='comments',
                             on_delete=models.CASCADE,
                             )
    author = models.ForeignKey(User,
                               related_name='comments',
                               on_delete=models.CASCADE,
                               )
    text = models.TextField('Текст комментария',
                            help_text='Введите текст комментария'
                            )
    created = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['author', 'user'],
                                               name='unique_follower')
                       ]

    class Meta:
        constraints = [models.UniqueConstraint(fields=['author', 'user'],
                                               name='unique_follower')
                       ]
