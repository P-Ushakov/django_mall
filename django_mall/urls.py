"""django_mall URL Configuration

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
from django.contrib import admin
from django.urls import path, include

# wagtail block
from django.conf import settings
from django.conf.urls.static import static

# wagtail block
from wagtail.core import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtailautocomplete.urls.admin import urlpatterns as autocomplete_admin_urls

urlpatterns = [
    path('mall/', include('mall.urls')),
    path('django-admin/', admin.site.urls),

    # wagtail block
    path('admin/autocomplete/', include(autocomplete_admin_urls)),
    path('admin/', include(wagtailadmin_urls)),
    path('docs/', include(wagtaildocs_urls)),
    path('', include(wagtail_urls)),
    # path('api/v2/', api_router.urls)
    # end of wagtail block
    # home page

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
