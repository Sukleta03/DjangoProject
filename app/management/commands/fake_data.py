from django.core.management.base import BaseCommand
from faker import Faker
import random
from app.models import User, Avatar, Post, Image, Tags

tag_list = ['food', 'travel', 'nature',
            'fashion', 'art', 'music',
            'sport', 'fitness', 'health',
            'beauty', 'lifestyle']


class Command(BaseCommand):
    help = 'Create fake data'

    def add_arguments(self, parser):
        parser.add_argument('num', type=int, nargs='?', default=1, help='Number of users to create')

    def handle(self, *args, **kwargs):
        fake = Faker()
        num = kwargs['num']

        for i in range(0, num):
            user = User.objects.create_user(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                password=fake.password(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                is_active=True
            )
            user.save()
            Avatar.objects.create(user=user, bio=user.first_name + " " + user.last_name)

            for i in range(0, 3):
                post = Post.objects.create(
                    user=user,
                    description=fake.text()
                )
                post.save()
                for tag in random.sample(tag_list, 2):
                    Tags.objects.create(
                        post=post,
                        tag=tag
                    )
                Image.objects.create(
                    post=post,
                    image='images/default.png'
                )

