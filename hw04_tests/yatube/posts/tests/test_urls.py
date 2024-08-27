from http import HTTPStatus

from django.test import Client, TestCase

from posts.models import Group, Post, User


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
        self.user = StaticURLTests.user
        self.authorized_client = Client()
        self.authorized_client.force_login(StaticURLTests.user)

    def test_404_uses_correct_template(self):
        response = self.client.get('/posts/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_private_url_exist_at_desired_location(self):
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_urls_auth_exist_desired_location(self):
        test_urls = {
            '/create/',
            f'/posts/{self.post.id}/edit/',
        }
        for page in test_urls:
            with self.subTest(page=page):
                response = self.authorized_client.get(page)
                self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_urls_exist_desired_location(self):
        test_urls = {
            '/',
            f'/group/{self.group.slug}/',
            f'/profile/{self.user.username}/',
            f'/posts/{self.post.id}/',
        }
        for page in test_urls:
            with self.subTest(page=page):
                response = self.client.get(page)
                self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_urls_uses_correct_template(self):
        test_urls = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user.username}/': 'posts/profile.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
            f'/posts/{self.post.id}/edit/': 'posts/update_post.html',
            '/create/': 'posts/create_post.html'
        }
        for page, template in test_urls.items():
            with self.subTest(page=page):
                response = self.authorized_client.get(page)
                self.assertTemplateUsed(response, template)
