from django.test import TestCase
from app.models import User, Avatar, Follow, Post, Image, Tags
from django.test import Client
from django.urls import reverse


class TestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='Ivan',
            password='12345678',
            email='ivan@test.ua',
            first_name='Ivan',
            last_name='Ivanov',
            is_active=True,
        )
        Avatar.objects.create(user=self.user, bio=self.user.first_name + " " + self.user.last_name)

        self.post = Post.objects.create(
            user=self.user,
            description='Test post'
        )

        self.image = Image.objects.create(
            post=self.post,
            image='images/default.png'
        )

        self.tags = Tags.objects.create(
            post=self.post,
            tag='test'
        )

        self.client = Client()

    def test_login(self):
        login = self.client.login(username='Ivan', password='12345678')
        self.assertTrue(login)

        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_homepage(self):
        self.client.login(username='Ivan', password='12345678')
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        self.client.login(username='Ivan', password='12345678')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

        self.client.post(reverse('profile'), {'email': 'ivan1@test.ua'})
        self.assertEqual(User.objects.get(username='Ivan').email, 'ivan1@test.ua')

    def test_user_profile(self):
        self.client.login(username='Ivan', password='12345678')
        response = self.client.get(reverse('user_profile', args=['Ivan']))
        self.assertEqual(response.status_code, 200)

    def test_follow(self):
        self.client.login(username='Ivan', password='12345678')

        self.client.get(reverse('follow', args=['Ivan']))
        self.assertEqual(Follow.objects.get(follower=self.user).following.username, 'Ivan')

    def test_new_post(self):
        self.client.login(username='Ivan', password='12345678')
        response = self.client.get('/new_post/')
        self.assertEqual(response.status_code, 200)

        self.client.post('/new_post/', {'description': 'test',
                                        'tag': 'test',
                                        })

        self.assertTrue(Post.objects.filter(user=self.user, description='test').exists())
        self.assertTrue(Tags.objects.filter(tag='test').exists())

        self.client.post('/new_post/', {})
        self.assertEqual(Post.objects.count(), 2) #пустой пост не создается



