from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("login/", views.login_func, name="login"),
    path("login/registration/", views.registration, name="registration"),
    path("login/registration/confirm/<int:id>/", views.confirm_email, name="confirm_email"),
    path('log_out/', views.log_out, name='log_out'),
    path("new_post/", views.new_post, name="new_post"),
    path('profile/', views.profile, name='profile'),
    path('confirm_email/<confirm_id>/', views.confirm_email, name='confirm_email'),
    path('reaction/', views.reaction, name='reaction'),
    path('user_profile/<str:username>', views.user_profile, name='user_profile'),
    path('follow/<str:username>', views.follow, name='follow'),
]
