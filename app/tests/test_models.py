from django.test import TestCase
from app.models import User, Avatar, ConfirmEmail, Follow, Post, Image, Tags, Reaction


class TestModels(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            username='Ivan',
            email='ivan@gmail.com',
            password='12345678',
            first_name='Ivan',
            last_name='Ivanov',
            is_active=True,
        )

        self.user2 = User.objects.create(
            username='Petr',
            email='petr@gmail.com',
            password='12345678',
            first_name='Petr',
            last_name='Petrov',
            is_active=True,
        )

        Avatar.objects.create(user=self.user1, bio=self.user1.first_name + " " + self.user1.last_name)
        Avatar.objects.create(user=self.user2, bio=self.user2.first_name + " " + self.user2.last_name)

        ConfirmEmail.objects.create(user=self.user1, email_id=123)
        ConfirmEmail.objects.create(user=self.user2, email_id=321)

        self.post = Post.objects.create(
            user=self.user1,
            description='Test post 1'
        )

    def test_user_model(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.username, 'Ivan')
        self.assertEqual(user.email, 'ivan@gmail.com')
        self.assertEqual(user.first_name, 'Ivan')
        self.assertEqual(user.last_name, 'Ivanov')

    def test_avatar_model(self):
        avatar = Avatar.objects.get(user=self.user1)
        self.assertEqual(avatar.user, self.user1)
        self.assertEqual(avatar.bio, 'Ivan Ivanov')

    def test_confirm_email_model(self):
        confimation = ConfirmEmail.objects.get(user=self.user1)
        self.assertEqual(confimation.user, self.user1)
        self.assertEqual(confimation.email_id, '123')

    def test_follow_model(self):
        Follow.objects.create(
            follower=self.user1,
            following=self.user2
        )
        Follow.objects.create(
            follower=self.user2,
            following=self.user1
        )

        self.assertTrue(Follow.objects.filter(follower=self.user1).exists())
        self.assertTrue(Follow.objects.filter(follower=self.user2).exists())

    def test_post_model(self):
        self.assertEqual(self.post.user, self.user1)

    def test_image_model(self):
        Image.objects.create(post=self.post, image='test_image.png')
        self.assertTrue(Image.objects.filter(post=self.post).exists())

    def test_tags_model(self):
        Tags.objects.create(post=self.post, tag='test')
        self.assertTrue(Tags.objects.filter(post=self.post).exists())

    def test_reaction_model(self):
        Reaction.objects.create(post=self.post, user=self.user1, reaction='like')
        self.assertTrue(Reaction.objects.filter(post=self.post).exists())

