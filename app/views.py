from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import User, Avatar, Post, Tags, Reaction, Image, Follow, ConfirmEmail
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.db.models import Count, Q
import json, string, random


@csrf_exempt
def login_func(request):
    if request.method == 'GET':
        return render(request, "login.html")
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('homepage'))
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, "login.html")


@csrf_exempt
def registration(request):
    if request.method == 'GET':
        return render(request, "registration.html")
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        is_active = False
        repeated_password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username is already taken')
            return render(request, "registration.html")

        if password == repeated_password:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name,
                                            is_active=is_active)

            confirm_id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=30))

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

            return render(request, 'confirm_email.html', {'email': user.email})


def confirm_email(request, confirm_id):
    if request.method == 'GET':
        user = ConfirmEmail.objects.get(email_id=confirm_id).user
        if user.is_active is False:
            user.is_active = True
            user.save()
            return redirect(reverse('login'))


def log_out(request):
    logout(request)
    return redirect(reverse('login'))


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


@login_required(login_url='/login/')
def profile(request):
    if request.method == 'GET':
        user = request.user
        return render(request, "profile.html", {'user': user})
    if request.method == 'POST':
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
            if not check_password(password, user.password):
                messages.error(request, 'Incorrect password')
                return render(request, "profile.html", {'user': user})
            new_password = request.POST.get('new_password')
            repeat_password = request.POST.get('new_password_repeat')
            if new_password != repeat_password:
                messages.error(request, 'Passwords do not match')
                return render(request, "profile.html", {'user': user})
            new_password = request.POST.get('new_password')
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password changed successfully')
        return render(request, "profile.html", {'user': user})


@login_required(login_url='/login/')
def homepage(request):
    user = request.user
    sorted_posts = Post.objects.annotate(
        num_likes=Count('reaction', filter=Q(reaction__reaction='like'))).order_by('-num_likes')
    posts = get_posts(sorted_posts)

    if request.method == 'GET':
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

    return render(request, "homepage.html", {'user': user, 'posts': posts})


def reaction(request):
    if request.method == 'POST':
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
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required(login_url='/login/')
def user_profile(request, username):
    if request.method == 'GET':
        user_data = get_user_data(username)
        return render(request, 'user_profile.html', {'user_data': user_data})


@login_required(login_url='/login/')
def new_post(request):
    user = request.user
    if request.method == 'POST':
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
    return render(request, "new_post.html")


@login_required(login_url='/login/')
def follow(request, username):
    if request.method == 'GET':
        following = User.objects.filter(username=username).first()
        is_followed = Follow.objects.filter(follower=request.user, following=following).exists()
        if is_followed:
            Follow.objects.filter(follower=request.user, following=following).delete()
        else:
            Follow.objects.create(follower=request.user, following=following)
        return redirect(reverse('user_profile', kwargs={'username': username}))












