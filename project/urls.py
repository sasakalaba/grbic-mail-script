from project import settings
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView


urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
