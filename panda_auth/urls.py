"""panda_auth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import (obtain_jwt_token,
                                      refresh_jwt_token,
                                      verify_jwt_token)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('docs/', include_docs_urls(title='Panda Auth API')),
    path('api-auth/', include('rest_framework.urls')),

    # jwt token
    path('jwt/auth/',    obtain_jwt_token),
    path('jwt/refresh/', refresh_jwt_token),
    path('jwt/verify/',  verify_jwt_token),

    # account
    path('account/', include('account.urls', namespace='account')),
]

if settings.DEBUG:
    # It is not necessary to add the urlpattern of static,
    # runerver will do this automatically when DEBUG is set to True.
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

