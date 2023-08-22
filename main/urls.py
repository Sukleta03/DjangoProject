"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("app.urls"), name="homepage"),
    path("", include("app.urls"), name="login"),
    path("", include("app.urls"), name="log_out"),
    path("", include("app.urls"), name="registration"),
    path("", include("app.urls"), name="confirm_email"),
    path("", include("app.urls"), name="new_post"),
    path("", include("app.urls"), name="profile"),
    path("", include("app.urls"), name="confirm_email"),
    path("", include("app.urls"), name="reaction"),
    path("", include("app.urls"), name="user_profile"),
    path("", include("app.urls"), name="follow"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

