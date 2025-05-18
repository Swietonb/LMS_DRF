"""
URL configuration for LMS_DRF project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

if TYPE_CHECKING:
    from drf_yasg.views import SchemaView

schema_view: SchemaView = get_schema_view(
   openapi.Info(
      title="Books API",
      default_version='v1',
   ),
   public=True,
)

urlpatterns: list[path] = [
    path("admin/", admin.site.urls),
    path("api/", include('apps.books.api.urls')),
    path("api/", include('apps.category.api.urls')),
    path("api/", include('apps.review.api.urls')),
    path("api/", include('apps.reservation.api.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
