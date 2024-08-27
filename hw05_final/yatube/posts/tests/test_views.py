from django import forms
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, Comment

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='test_user')
        cls.group = Group.objects.create(
            title='Text_group',
            slug='test_slug',
            description='Test_description',
        )
        cls.another_group = Group.objects.create(
            title='Text_group_another',
            slug='test_slug_another',
            description='Test_description_another',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Test_text',
            group=(Group.objects.get(slug='test_slug'))
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse('posts:group_list',
                                             kwargs={'slug': 'test_slug'}),
            'posts/profile.html': reverse(
                'posts:profile', kwargs={'username': 'test_user'}),
            'posts/post_detail.html': reverse(
                'posts:post_detail', kwargs={'post_id': '1'}),
            'posts/create_post.html': reverse('posts:post_create'),
        }

        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_home_page_show_correct_contex(self):
        response = self.authorized_client.get(reverse('posts:index'))
        test_object = response.context['page_obj'][0]
        contex = {
            self.user: test_object.author,
            self.post.text: test_object.text,
            self.post.group: test_object.group,
            self.post.id: test_object.id,

        }
        for reverse_name, response_name in contex.items():
            with self.subTest(reverse_name=reverse_name):
                self.assertEqual(response_name, reverse_name)

    def test_group_list_page_show_correct_contex(self):
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test_slug'}))
        for post in response.context['page_obj']:
            self.assertEqual(post.group, self.group)

    def test_profile_page_show_correct_contex(self):
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': 'test_user'}))
        for post in response.context['page_obj']:
            self.assertEqual(post.author, self.user)

    def test_post_detail_page_show_correct_contex(self):
        response = self.authorized_client.get(reverse(
            'posts:post_detail', kwargs={'post_id': '1'})
        ).context['post']
        self.assertEqual(response, self.post)

    def test_create_page_show_correct_contex(self):
        response = self.authorized_client.get(
            reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_page_show_correct_contex(self):
        response = self.authorized_client.get(
            reverse('posts:post_edit',
                    kwargs={'post_id': PostURLTests.post.id},
                    ))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_new_create_correct_in_pages(self):
        new_post = Post.objects.create(
            author=self.user,
            text=self.post.text,
            group=self.group
        )
        pages = [
            reverse('posts:index'),
            reverse(
                'posts:group_list', kwargs={'slug': self.group.slug}),
            reverse(
                'posts:profile', kwargs={'username': self.user.username})
        ]
        for rev in pages:
            with self.subTest(rev=rev):
                response = self.authorized_client.get(rev)
                self.assertIn(
                    new_post, response.context['page_obj']
                )

    def test_new_post_not_in_group(self):
        new_post = Post.objects.create(
            author=self.user,
            text=self.post.text,
            group=self.group
        )
        response = self.authorized_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': self.another_group.slug})
        )
        self.assertNotIn(new_post, response.context['page_obj'])

    def test_images_appears_in_pages(self):
        posts_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        self.post_with_image = Post.objects.create(
            author=self.user,
            text='test with image',
            group=self.group,
            image=uploaded
        )
        urls = (
            reverse('posts:index'),
            reverse('posts:profile', kwargs={'username': self.user}),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        for url in urls:
            with self.subTest(url=url):
                self.authorized_client.get(url)
                self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_add_comment(self):
        comment_count = Comment.objects.count()
        form = {
            'post': self.post,
            'author': self.user,
            'text': self.post.text,
        }
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.user.id}),
            data=form,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}))
        comment = Comment.objects.first()
        self.assertEqual(Comment.objects.count(), comment_count + 1)
        self.assertEqual(str(comment.post), self.post.text)
        self.assertEqual(comment.text, form['text'])
        self.assertEqual(comment.author, self.post.author)


class CashTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username='test_user')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.post = Post.objects.create(
            author=self.user,
            text='test_cashe'
        )

    def test_caching(self):
        response = self.client.get(reverse('posts:index'))
        cache_new = response.content
        Post.objects.filter(text='test_cashe').delete()
        response = self.client.get(reverse('posts:index'))
        cache_after_delete = response.content
        self.assertEqual(cache_new, cache_after_delete)
        cache.clear()
        response = self.client.get(reverse('posts:index'))
        cache_after_clear = response.content
        self.assertNotEqual(cache_after_clear, cache_new)


class ErrorUrlTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_404_page_not_found(self):
        response = self.client.get('fake_url/')
        self.assertEqual(response.status_code, 404)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='test_author')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug',
            description='Описание группы',
        )
        number_of_posts = 13
        cls.posts = []
        for post_id in range(number_of_posts):
            post = Post.objects.create(
                text=f'Тестовый пост {post_id}',
                author=cls.author,
                group=cls.group,
            )
            cls.posts.append(post)
        cls.urls_with_paginator = [
            reverse('posts:index'),
            reverse('posts:profile', args={cls.author.username}),
            reverse('posts:group_list', args={cls.group.slug}),
        ]

    def setUp(self):
        self.authorized_author = Client()
        self.authorized_author.force_login(self.author)

    def test_first_page_contains_ten_records(self):
        for reverse_name in self.urls_with_paginator:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_author.get(reverse_name)
                self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_three_records(self):
        for reverse_name in self.urls_with_paginator:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_author.get(
                    reverse_name + '?page=2')
                self.assertEqual(len(response.context['page_obj']), 3)
