
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

API_VERS = 'api/v1'


urlpatterns = [
    path(f'{API_VERS}/admin/', admin.site.urls),
    path(f'{API_VERS}/', include('users.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


