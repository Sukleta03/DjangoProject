from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Count, Q
from django.http import JsonResponse
import json, string, random
from django.utils.decorators import method_decorator
from .models import User, Avatar, Post, Tags, Reaction, Image, Follow, ConfirmEmail
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import *


@method_decorator(csrf_exempt, name='dispatch')
class Login(View):
    form = LoginForm()

    def get(self, request):
        return render(request, "login.html", {"form": self.form})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('homepage'))
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, "login.html", {"form": self.form})


@method_decorator(csrf_exempt, name='dispatch')
class Registration(View):
    form = RegistrationForm()

    def get(self, request):
        return render(request, "registration.html", {"form": self.form})

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        is_active = False
        repeated_password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username is already taken')
            return render(request, "registration.html", {"form": self.form})

        if password == repeated_password:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name,
                                            is_active=is_active)

            confirm_id = ''.join(
                random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=30))

            confimation = ConfirmEmail.objects.create(user=user, email_id=confirm_id)
            bio = first_name + " " + last_name
            avatar = Avatar.objects.create(user=user, bio=bio)

            http_host = request.META.get('HTTP_HOST')
            url = f'{request.scheme}://{http_host}/confirm_email/{confirm_id}'
            subject = 'Сonfirm your registration'
            message = f'Сonfirm your registration \n {url}'
            from_email = 'dima.sukleta03@gmail.com'
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list)

            return render(request, "confirm_email.html", {"email": user.email})


@method_decorator(csrf_exempt, name='dispatch')
class Confirmation(View):
    def get(self, confirm_id):
        user = ConfirmEmail.objects.get(email_id=confirm_id).user
        if user.is_active is False:
            user.is_active = True
            user.save()
            return redirect(reverse('login'))


@method_decorator(login_required(login_url='/login/'), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class Profile(View):

    def get(self, request):
        user = request.user
        return render(request, "profile.html", {'user': user})

    def post(self, request):
        user = request.user
        if request.FILES.get('avatar'):
            avatar_img = request.FILES.get('avatar')
            user.avatar.avatar = avatar_img
            user.avatar.save()
        if request.POST.get('first_name') and request.POST.get('last_name'):
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            bio = first_name + " " + last_name
            user.avatar.bio = bio
            user.first_name = first_name
            user.last_name = last_name
            user.save(), user.avatar.save()
        if request.POST.get('email'):
            if User.objects.filter(email=request.POST.get('email')).exists():
                messages.error(request, 'This email is already taken')
                return render(request, "profile.html", {'user': user})
            email = request.POST.get('email')
            user.email = email
            user.save()
        if request.POST.get('password'):
            password = request.POST.get('password')
            user.set_password(password)
            user.save()
        return redirect(reverse('profile'))


@method_decorator(login_required(login_url='/login/'), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class UserProfile(View):

    def get(self, request, username):
        user_data = get_user_data(username)
        return render(request, 'user_profile.html', {'user_data': user_data})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class FollowView(View):
    def get(self, request, username):
        following = User.objects.filter(username=username).first()
        is_followed = Follow.objects.filter(follower=request.user, following=following).exists()
        if is_followed:
            Follow.objects.filter(follower=request.user, following=following).delete()
        else:
            Follow.objects.create(follower=request.user, following=following)
        return redirect(reverse('user_profile', kwargs={'username': username}))

    #     @login_required(login_url='/login/')
    #     def follow(request, username):
    #         if request.method == 'GET':
    #             following = User.objects.filter(username=username).first()
    #             is_followed = Follow.objects.filter(follower=request.user, following=following).exists()
    #             if is_followed:
    #                 Follow.objects.filter(follower=request.user, following=following).delete()
    #             else:
    #                 Follow.objects.create(follower=request.user, following=following)
    #             return redirect(reverse('user_profile', kwargs={'username': username}))


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class Homepage(View):
    def get(self, request):
        user = request.user
        if request.GET.get('sort'):
            sort = request.GET.get('sort')
            if sort == 'likes':
                sorted_posts = Post.objects.annotate(
                    num_likes=Count('reaction', filter=Q(reaction__reaction='like'))).order_by('-num_likes')
                posts = get_posts(sorted_posts)

            if sort == 'my_posts':
                posts = get_posts(Post.objects.filter(user=user))

            if sort == 'by_tag':
                tag = request.GET.get('tag')
                if tag:
                    posts = get_posts(Post.objects.filter(tags__tag=tag))
                else:
                    posts = get_posts(Post.objects.all())

            if sort == 'following':
                posts = []
                follow_list = [x for x in Follow.objects.filter(follower=user)]
                for follow_obj in follow_list:
                    posts.extend(get_posts(Post.objects.filter(user=follow_obj.following)))

        else:
            sorted_posts = Post.objects.annotate(
                num_likes=Count('reaction', filter=Q(reaction__reaction='like'))).order_by('-num_likes')
            posts = get_posts(sorted_posts)

        return render(request, "homepage.html", {'user': user, 'posts': posts})


class Reactions(View):
    def post(self, request):
        reaction_type = json.loads(request.body).get('reaction_type')
        post_id = json.loads(request.body).get('post_id')
        post = Post.objects.filter(post_id=post_id).first()

        reaction_obj = Reaction.objects.filter(post=post, user=request.user).first()

        if reaction_obj:
            if reaction_type == reaction_obj.reaction:
                pass
            else:
                reaction_obj.reaction = reaction_type
                reaction_obj.save()
        else:
            reaction_obj = Reaction.objects.create(post=post, user=request.user, reaction=reaction_type)
            reaction_obj.save()

        likes = Reaction.objects.filter(post=post, reaction='like').count()
        dislikes = Reaction.objects.filter(post=post, reaction='dislike').count()

        data = {
            'like_count': likes,
            'dislike_count': dislikes,
        }
        return JsonResponse(data)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class NewPost(View):
    def get(self, request):
        return render(request, "new_post.html")

    def post(self, request):
        user = request.user
        if request.FILES.getlist('images') or request.POST.get('description'):
            images = request.FILES.getlist('images')
            description = request.POST.get('description')
            tags = request.POST.getlist('tags')
            post = Post.objects.create(user=user, description=description)
            for image in images:
                Image.objects.create(post=post, image=image)
            for tag in tags:
                Tags.objects.create(post=post, tag=tag)
            return redirect(reverse('homepage'))
        else:
            messages.error(request, 'Post is empty')
            return render(request, "new_post.html")


def get_posts(posts):
    post_list = []
    for post in posts:
        likes = Reaction.objects.filter(post=post, reaction='like').count()
        dislikes = Reaction.objects.filter(post=post, reaction='dislike').count()
        post_id = post.post_id
        username = post.user.username
        avatar = post.user.avatar
        images = [x for x in Image.objects.filter(post=post)]
        description = post.description
        created_at = post.created_at
        tags = Tags.objects.filter(post=post)
        post_list.append({
            'post_id': post_id,
            'username': username,
            'avatar': avatar,
            'images': images,
            'description': description,
            'created_at': created_at,
            'tags': tags,
            'likes': likes,
            'dislikes': dislikes
        })
    return post_list


def get_user_data(username):
    user = User.objects.get(username=username)
    user_posts = get_posts(Post.objects.filter(user=user))
    user_avatar = user.avatar
    user_followers = Follow.objects.filter(following=user).count()
    user_following = Follow.objects.filter(follower=user).count()
    return {
        'user': user,
        'user_posts': user_posts,
        'avatar': user_avatar,
        'user_followers': user_followers,
        'user_following': user_following,
    }


def log_out(request):
    logout(request)
    return redirect(reverse('login'))


