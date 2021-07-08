# deals/tests/tests_models.py
from django.test import TestCase
from posts.models import Post, Group
from django.db import models
from django.contrib.auth import get_user_model

class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        #super().setUpClass()
    
        cls.Post = Post.objects.create(
            text='Тестовый текст',
            pub_date = '02.04.2020',
        )

    def test_object_name_is_title_fild(self):
        """В поле __str__  объекта task записано значение поля task.title."""
        post = PostModelTest.Post
        context = {
            'text':'Тестовый текст',
            'pub_date' : '02.04.2020',
        }
        self.assertEqual(post, context, 'err')
