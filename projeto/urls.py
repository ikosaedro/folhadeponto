
from django.contrib import admin
from django.urls import path, include;
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('folhadeponto.urls')),
    path('sair/', auth_views.LogoutView.as_view(), name='sair'),
    path('accounts/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)