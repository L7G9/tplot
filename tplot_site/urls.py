"""
URL configuration for tplot_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
import user_guide.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("timelines/", include("timelines.urls")),
    path("timelines/age/", include("age_timelines.urls")),
    path("timelines/datetime/", include("date_time_timelines.urls")),
    path("timelines/historical/", include("historical_timelines.urls")),
    path("timelines/scientific/", include("scientific_timelines.urls")),
    path("user_guide/", include("user_guide.urls")),
    path("", user_guide.views.home),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
