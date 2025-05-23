from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.urls import include, path, reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', include('blog.urls', namespace='blog')),
    path(
        'admin/login/',
        RedirectView.as_view(
            url=settings.LOGIN_URL, permanent=True, query_string=True
        )
    ),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('blog:index'),
        ),
        name='registration',
    ),
    path('pages/', include('pages.urls', namespace='pages')),
]

handler404 = 'pages.views.page404'
handler500 = 'pages.views.page500'

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
