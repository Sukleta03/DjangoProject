from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField


class Avatar(models.Model):

    class Meta:
        db_table = 'avatar'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='')
    avatar = CloudinaryField('avatar', folder='avatar', default='avatar/default_y8l4fd.png')
    # avatar = models.ImageField(upload_to='images/avatars/', default='images/avatars/default.png')


class ConfirmEmail(models.Model):

    class Meta:
        db_table = 'confirm_email'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_id = models.CharField(max_length=256, blank=True, null=True)


class Follow(models.Model):

    class Meta:
        db_table = 'follow'

    follower = models.ForeignKey(User, on_delete=models.PROTECT, related_name='follower', db_column='follower')
    following = models.ForeignKey(User, on_delete=models.PROTECT, related_name='following', db_column='following')


class Post(models.Model):

    class Meta:
        db_table = 'post'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=500, blank=True)


class Image(models.Model):

    class Meta:
        db_table = 'image'

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='images/', default='images/default.png')
    image = CloudinaryField('images', default='default_snkrnb.png')


class Tags(models.Model):

    class Meta:
        db_table = 'tags'

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.CharField(max_length=50)


class Reaction(models.Model):

    class Meta:
        db_table = 'reaction'
        unique_together = ('user', 'post')

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=50)