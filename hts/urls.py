from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.decorators.http import last_modified
from django.views.i18n import JavaScriptCatalog

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.images.views.serve import ServeView

from hts.search import views as search_views



from misago.users.forms.auth import AdminAuthenticationForm


admin.autodiscover()
admin.site.login_form = AdminAuthenticationForm

urlpatterns = [
    url(r'^django-admin/', admin.site.urls),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    # Javascript translations
    url(
        r"^django-i18n.js$",
        last_modified(lambda req, **kw: timezone.now())(
            cache_page(86400 * 2, key_prefix="misagojsi18n")(
                JavaScriptCatalog.as_view(packages=["misago"])
            )
        ),
        name="django-i18n",
    ),

    url(r'^search/$', search_views.search, name='search'),
    url(r'^community/', include("misago.urls", namespace="misago")),
    url(r'^images/([^/]*)/(\d*)/([^/]*)/[^/]*$', ServeView.as_view(), name='wagtailimages_serve'),

    # django-simple-sso doesn't have namespaces, we can't use namespace here
    url(r"^sso/", include("misago.sso.urls")),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.urls import path

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r"", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r"^pages/", include(wagtail_urls)),
]
