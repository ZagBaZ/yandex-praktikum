import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Group, Post, User

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Dima')

        cls.group = Group.objects.create(
            title='test_title',
            description='test_description',
            slug='test_slug',
        )

        cls.post = Post.objects.create(
            author=cls.user,
            text='test_text',
            group=cls.group,
        )

        cls.other_post = Post.objects.create(
            author=cls.user,
            text='test_text',
            group=cls.group,
        )

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.new_uploaded = SimpleUploadedFile(
            name='new_small.gif',
            content=small_gif,
            content_type='image/gif'
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': self.post.text,
            'group': self.group.pk,
            'image': self.uploaded,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse('posts:profile', kwargs={
            'username': self.user}))

        test_object = Post.objects.order_by("-id").first()
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(test_object.text, form_data['text'])
        self.assertEqual(test_object.group.pk, form_data['group'])
        self.assertEqual(test_object.image, 'posts/small.gif')

    def test_edit_post(self):
        new_form_data = {
            'text': self.post.text,
            'group': self.group.pk,
        }

        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=new_form_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse(
                'posts:post_detail', kwargs={'post_id': self.post.id})
        )
        new_test_object = Post.objects.order_by("-id").first()
        self.assertEqual(new_test_object.text, new_form_data['text'])
        self.assertEqual(new_test_object.group.pk, new_form_data['group'])
