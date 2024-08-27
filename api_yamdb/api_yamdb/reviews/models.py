from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User
from titles.models import Title


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(10)),
        error_messages={'validators': 'Оценка от 1 до 10!'},)
    pub_date = models.DateTimeField('Дата написания отзыва', auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author', ],
                name='unique_reviews'
            ),
        ]
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата написания комментария', auto_now_add=True)

    def __str__(self):
        return self.text
