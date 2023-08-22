from django.urls import path

from . import views

urlpatterns = [
    path("", views.Homepage.as_view(), name="homepage"),
    path("login/", views.Login.as_view(), name="login"),
    path("login/registration/", views.Registration.as_view(), name="registration"),
    path("confirm_email/<confirm_id>", views.Confirmation.as_view(), name="confirm_email"),
    path('log_out/', views.log_out, name='log_out'),
    path("new_post/", views.NewPost.as_view(), name="new_post"),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('reaction/', views.Reactions.as_view(), name='reaction'),
    path('user_profile/<str:username>', views.UserProfile.as_view(), name='user_profile'),
    path('follow/<str:username>', views.FollowView.as_view(), name='follow'),
]