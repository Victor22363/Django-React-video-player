from django.contrib import admin
from django.urls import path, include
from one import urls
from django.conf import settings
from django.conf.urls.static import static
from one.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('watch/', include("one.urls"))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)