from http import HTTPStatus

from django.test import TestCase, Client
from posts.models import User, Group, Post


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create(username='Dima')

        cls.group = Group.objects.create(
            title='текстовый заголовок',
            slug='test_slug',
            description='тестовое описание'
        )

        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый текст',
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        self.user = StaticURLTests.user
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(StaticURLTests.user)

    def test_homepage_url_exist_at_desired_location(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_homepage_url_uses_correct_template(self):
        response = self.guest_client.get('/')
        self.assertTemplateUsed(response, 'posts/index.html')

    def test_group_url_exist_at_desired_location(self):
        response = self.guest_client.get('/group/test_slug/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_group_url_uses_correct_template(self):
        response = self.guest_client.get('/group/test_slug/')
        self.assertTemplateUsed(response, 'posts/group_list.html')

    def test_profile_url_exist_at_desired_location(self):
        response = self.guest_client.get('/profile/Dima/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_url_uses_correct_template(self):
        response = self.guest_client.get('/profile/Dima/')
        self.assertTemplateUsed(response, 'posts/profile.html')

    def test_posts_url_exist_at_desired_location(self):
        response = self.guest_client.get('/posts/1/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_uses_correct_template(self):
        response = self.guest_client.get('/posts/1/')
        self.assertTemplateUsed(response, 'posts/post_detail.html')

    def test_404_uses_correct_template(self):
        response = self.guest_client.get('/posts/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_create_url_exist_at_desired_location(self):
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_uses_correct_template(self):
        response = self.authorized_client.get('/create/')
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_edit_url_exist_at_desired_location(self):
        response = self.authorized_client.get(f'/posts/{self.post.id}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_uses_correct_template(self):
        response = self.authorized_client.get(f'/posts/{self.post.id}/edit/')
        self.assertTemplateUsed(response, 'posts/update_post.html')

    def test_private_url_exist_at_desired_location(self):
        response = self.guest_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
