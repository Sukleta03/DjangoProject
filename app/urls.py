from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomePageViews.homepage, name="homepage"),
    path("login/", views.UserViews.login_func, name="login"),
    path("login/registration/", views.UserViews.registration, name="registration"),
    path("login/registration/confirm/<int:id>/", views.UserViews.confirm_email, name="confirm_email"),
    path('log_out/', views.UserViews.log_out, name='log_out'),
    path("new_post/", views.NewPostViews.new_post, name="new_post"),
    path('profile/', views.ProfileViews.profile, name='profile'),
    path('confirm_email/<confirm_id>/', views.UserViews.confirm_email, name='confirm_email'),
    path('reaction/', views.HomePageViews, name='reaction'),
    path('user_profile/<str:username>', views.ProfileViews.user_profile, name='user_profile'),
    path('follow/<str:username>', views.ProfileViews.follow, name='follow'),
]