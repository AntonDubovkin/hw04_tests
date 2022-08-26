from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_verbose_name_group(self):
        """Verbose_name полях совпадает group с ожиданиями"""
        group = PostModelTest.group
        field_verboses = {
            'title': 'Заголовок',
            'description': 'Описание',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).verbose_name, expected_value
                )

    def test_verbose_name_post(self):
        """Verbose_name полях post совпадает с ожиданиями"""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value
                )

    def test_help_text_post(self):
        """Help_text в полях post совпадает с ожиданием"""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Группа, относительно поста',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected
                )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__"""
        group = PostModelTest.group
        post = PostModelTest.post
        expected_objects_name_group = group.title
        expected_objects_name_post = post.text[:15]
        self.assertEqual(expected_objects_name_group, str(group))
        self.assertEqual(expected_objects_name_post, str(post))
