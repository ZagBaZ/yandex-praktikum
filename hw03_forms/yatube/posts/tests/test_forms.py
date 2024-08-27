import shutil
import tempfile

from django.contrib.auth import get_user_model
from ..forms import PostForm
from ..models import Post, Group, User
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TaskCreateFormTests(TestCase):
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

        cls.form = PostForm()

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
            'image': self.uploaded.name,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )

        self.assertRedirects(response, reverse('posts:profile', kwargs={
            'username': self.user}))

        self.assertEqual(Post.objects.count(), posts_count + 1)
        test_object = Post.objects.order_by("-id").first()
        self.assertEqual(form_data['text'], test_object.text)
        self.assertEqual(form_data['group'], test_object.group.pk)
        self.assertEqual(form_data['image'], self.uploaded.name)

    def test_edit_post(self):
        form_data = {
            'text': self.post.text,
            'group': self.group.pk,
            'image': self.uploaded.name,

        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse(
                'posts:post_detail', kwargs={'post_id': self.post.id})
        )
        self.assertEqual(form_data['text'], self.post.text)
        self.assertEqual(form_data['group'], self.group.pk)
        self.assertEqual(form_data['image'], self.uploaded.name)
