from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

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
            'posts/update_post.html': reverse(
                'posts:post_edit', kwargs={'post_id': '1'}),
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
