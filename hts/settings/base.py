"""
Django settings for hts project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from misago import load_plugin_list_if_exists


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


# Application definition


AUTHENTICATION_BACKENDS = ["misago.users.authbackends.MisagoBackend"]

CSRF_FAILURE_VIEW = "misago.core.errorpages.csrf_failure"

PLUGINS_LIST_PATH = os.path.join(os.path.dirname(BASE_DIR), "plugins.txt")

INSTALLED_PLUGINS = load_plugin_list_if_exists(PLUGINS_LIST_PATH) or []

INSTALLED_APPS = INSTALLED_PLUGINS + [

    # Misago overrides for Django core feature
    "misago",
    "misago.users",

    # our pages
    'hts.base',
    'hts.search',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.modeladmin',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    'modelcluster',
    'taggit',
    'django_extensions',
    'bootstrap4',

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.postgres",
    "django.contrib.humanize",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # 3rd party apps used by Misago
    "ariadne.contrib.django",
    "celery",
    "debug_toolbar",
    "mptt",
    "rest_framework",
    "social_django",
    # Misago apps
    "misago.admin",
    "misago.acl",
    "misago.analytics",
    "misago.cache",
    "misago.core",
    "misago.conf",
    "misago.icons",
    "misago.themes",
    "misago.markup",
    "misago.legal",
    "misago.categories",
    "misago.threads",
    "misago.readtracker",
    "misago.search",
    "misago.socialauth",
    "misago.graphql",
    "misago.faker",
    "misago.menus",
    "misago.sso",
    "misago.plugins",

    # Menus
    'wagtailmenus',

    # Design / CSS
    'sass_processor',
    'compressor',
]

AUTH_USER_MODEL = "misago_users.User"

LOGIN_REDIRECT_URL = "wagtailadmin_home"

LOGIN_URL = "misago:login"

LOGOUT_URL = "misago:logout"

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "misago.users.middleware.RealIPMiddleware",
    "misago.core.middleware.FrontendContextMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "misago.cache.middleware.cache_versions_middleware",
    "misago.conf.middleware.dynamic_settings_middleware",
    "misago.socialauth.middleware.socialauth_providers_middleware",
    "misago.users.middleware.UserMiddleware",
    "misago.acl.middleware.user_acl_middleware",
    "misago.core.middleware.ExceptionHandlerMiddleware",
    "misago.users.middleware.OnlineTrackerMiddleware",
    "misago.admin.middleware.AdminAuthMiddleware",
    "misago.threads.middleware.UnreadThreadsCountMiddleware",
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'hts.urls'

SOCIAL_AUTH_STRATEGY = "misago.socialauth.strategy.MisagoStrategy"

SOCIAL_AUTH_PIPELINE = (
    # Steps required by social pipeline to work - don't delete those!
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.social_user",
    # If enabled in admin panel, lets your users to associate their old forum account
    # with social one, if both have same e-mail address.
    "misago.socialauth.pipeline.associate_by_email",
    # Those steps make sure banned users may not join your site or use banned name or email.
    "misago.socialauth.pipeline.validate_ip_not_banned",
    "misago.socialauth.pipeline.validate_user_not_banned",
    # Reads user data received from social site and tries to create valid and available username
    # Required if you want automatic account creation to work. Otherwise optional.
    "misago.socialauth.pipeline.get_username",
    # Uncomment next line to enable automatic account creation if data from social site is valid
    # and get_username found valid name for new user account:
    # 'misago.socialauth.pipeline.create_user',
    # This step asks user to complete simple, pre filled registration form containing username,
    # email, legal note if you remove it without adding custom one, users will have no fallback
    # for joining your site using their social account.
    "misago.socialauth.pipeline.create_user_with_form",
    # Steps finalizing social authentication flow - don't delete those!
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "misago.socialauth.pipeline.require_activation",
)

SOCIAL_AUTH_POSTGRES_JSONFIELD = True


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'wagtail.contrib.settings.context_processors.settings',

                # menus
                'wagtailmenus.context_processors.wagtailmenus',

                "misago.acl.context_processors.user_acl",
                "misago.conf.context_processors.conf",
                "misago.conf.context_processors.og_image",
                "misago.core.context_processors.misago_version",
                "misago.core.context_processors.request_path",
                "misago.core.context_processors.momentjs_locale",
                "misago.icons.context_processors.icons",
                "misago.search.context_processors.search_providers",
                "misago.themes.context_processors.theme",
                "misago.legal.context_processors.legal_links",
                "misago.menus.context_processors.menus",
                "misago.users.context_processors.user_links",
                "misago.core.context_processors.hooks",
                # Data preloaders
                "misago.conf.context_processors.preload_settings_json",
                "misago.core.context_processors.current_link",
                "misago.markup.context_processors.preload_api_url",
                "misago.threads.context_processors.preload_threads_urls",
                "misago.users.context_processors.preload_user_json",
                "misago.socialauth.context_processors.preload_socialauth_json",
                # Note: keep frontend_context processor last for previous processors
                # to be able to expose data UI app via request.frontend_context
                "misago.core.context_processors.frontend_context",
            ]
        },
    }
]

WSGI_APPLICATION = 'hts.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "hts_dev",
        "HOST": "localhost",
        "PORT": 5432
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



# Django Rest Framework
# http://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "misago.core.rest_permissions.IsAuthenticatedOrReadOnly"
    ],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "EXCEPTION_HANDLER": "misago.core.exceptionhandler.handle_api_exception",
    "UNAUTHENTICATED_USER": "misago.users.models.AnonymousUser",
    "URL_FORMAT_OVERRIDE": None,
}


# Celery - Distributed Task Queue
# http://docs.celeryproject.org/en/latest/userguide/configuration.html

# Configure Celery to use Redis as message broker.

CELERY_BROKER_URL = "redis://redis:6379/0"

# Celery workers may leak the memory, eventually depriving the instance of resources.
# This setting forces celery to stop worker, clean after it and create new one
# after worker has processed 10 tasks.

CELERY_WORKER_MAX_TASKS_PER_CHILD = 10

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# INTERNAL_IPS = [
#     '127.0.0.1',
# ]

# Caching
# https://docs.djangoproject.com/en/1.11/topics/cache/#setting-up-the-cache
MISAGO_SEARCH_CONFIG = "german"
CACHES = {
    "default": {
        # Misago doesn't run well with LocMemCache in production environments
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache"
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)


STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# Javascript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/3.0/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Wagtail settings

WAGTAIL_SITE_NAME = "hts"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://example.com'
