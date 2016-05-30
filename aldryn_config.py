# -*- coding: utf-8 -*-
import json
import os
import sys
from aldryn_client import forms

SYSTEM_FIELD_WARNING = 'WARNING: this field is auto-written. Please do not change it here.'


class Form(forms.BaseForm):
    languages = forms.CharField(
        'Languages',
        required=True,
        initial='["en", "de"]',
        help_text=SYSTEM_FIELD_WARNING,
    )

    def to_settings(self, data, settings):
        import dj_database_url
        import warnings
        from functools import partial
        from aldryn_addons.utils import boolean_ish, djsenv
        env = partial(djsenv, settings=settings)

        # BASE_DIR should already be set by aldryn-addons
        settings['BASE_DIR'] = env('BASE_DIR', required=True)
        settings['DATA_ROOT'] = env('DATA_ROOT', os.path.join(settings['BASE_DIR'], 'data'))
        settings['SECRET_KEY'] = env('SECRET_KEY', 'this-is-not-very-random')
        settings['DEBUG'] = boolean_ish(env('DEBUG', False))

        settings['DATABASE_URL'] = env('DATABASE_URL')
        settings['CACHE_URL'] = env('CACHE_URL')
        if env('DJANGO_MODE') == 'build':
            # In build mode we don't have any connected services like db or
            # cache available. So we need to configure those things in a way
            # they can run without real backends.
            settings['DATABASE_URL'] = 'sqlite://:memory:'
            settings['CACHE_URL'] = 'locmem://'

        if not settings['DATABASE_URL']:
            settings['DATABASE_URL'] = 'sqlite:///{}'.format(
                os.path.join(settings['DATA_ROOT'], 'db.sqlite3')
            )
            warnings.warn(
                'no database configured. Falling back to DATABASE_URL={0}'.format(
                    settings['DATABASE_URL']
                ),
                RuntimeWarning,
            )
        if not settings['CACHE_URL']:
            settings['CACHE_URL'] = 'locmem://'
            warnings.warn(
                'no cache configured. Falling back to CACHE_URL={0}'.format(
                    settings['CACHE_URL']
                ),
                RuntimeWarning,
            )

        settings['DATABASES']['default'] = dj_database_url.parse(settings['DATABASE_URL'])

        settings['ROOT_URLCONF'] = env('ROOT_URLCONF', 'urls')
        settings['ADDON_URLS'].append('aldryn_django.urls')
        settings['ADDON_URLS_I18N'].append('aldryn_django.i18n_urls')

        settings['WSGI_APPLICATION'] = 'wsgi.application'

        settings['INSTALLED_APPS'].extend([
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.admin',
            'django.contrib.staticfiles',
            'aldryn_django',
        ])

        settings['TEMPLATES'] = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': env('TEMPLATE_DIRS', [os.path.join(settings['BASE_DIR'], 'templates')], ),
                'OPTIONS': {
                    'debug': boolean_ish(env('TEMPLATE_DEBUG', settings['DEBUG'])),
                    'context_processors': [
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                        'django.core.context_processors.i18n',
                        'django.core.context_processors.debug',
                        'django.core.context_processors.request',
                        'django.core.context_processors.media',
                        'django.core.context_processors.csrf',
                        'django.core.context_processors.tz',
                        'django.core.context_processors.static',
                        'aldryn_django.context_processors.debug',
                    ],
                    'loaders': [
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                        'django.template.loaders.eggs.Loader',
                    ],
                },
            },
        ]

        settings['MIDDLEWARE_CLASSES'] = [
            'django.contrib.sessions.middleware.SessionMiddleware',
            # 'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'django.contrib.sites.middleware.CurrentSiteMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            # 'django.middleware.security.SecurityMiddleware',
        ]

        settings['SITE_ID'] = env('SITE_ID', 1)

        settings['ADDON_URLS_I18N_LAST'] = 'aldryn_django.urls_redirect'

        self.domain_settings(data, settings, env=env)
        self.security_settings(data, settings, env=env)
        self.server_settings(settings, env=env)
        self.logging_settings(settings, env=env)
        # Order matters, sentry settings rely on logging being configured.
        self.sentry_settings(settings, env=env)
        self.cache_settings(settings, env=env)
        self.storage_settings_for_media(settings, env=env)
        self.storage_settings_for_static(settings, env=env)
        self.i18n_settings(data, settings, env=env)
        self.migration_settings(settings, env=env)
        return settings

    def domain_settings(self, data, settings, env):
        settings['ALLOWED_HOSTS'] = env('ALLOWED_HOSTS', ['localhost', '*'])
        # will take a full config dict from ALDRYN_SITES_DOMAINS if available,
        # otherwise fall back to constructing the dict from DOMAIN,
        # DOMAIN_ALIASES and DOMAIN_REDIRECTS
        domains = env('ALDRYN_SITES_DOMAINS', {})
        domain = env('DOMAIN')
        if domain:
            settings['DOMAIN'] = domain
        domain_aliases = env('DOMAIN_ALIASES', '')
        domain_redirects = env('DOMAIN_REDIRECTS', '')
        if not domains and domain:
            domains = {
                1: {
                    'name': env('SITE_NAME', ''),
                    'domain': domain,
                    'aliases': [d.strip() for d in domain_aliases.split(',') if d.strip()],
                    'redirects': [d.strip() for d in domain_redirects.split(',') if d.strip()]
                }
            }
        settings['ALDRYN_SITES_DOMAINS'] = domains
        if domains and settings['SITE_ID'] in domains:
            settings['ALLOWED_HOSTS'].extend([
                domain for domain in domains[settings['SITE_ID']]['aliases']
            ] + [
                domain for domain in domains[settings['SITE_ID']]['redirects']
            ])

        settings['INSTALLED_APPS'].append('aldryn_sites')
        settings['MIDDLEWARE_CLASSES'].insert(
            settings['MIDDLEWARE_CLASSES'].index('django.middleware.common.CommonMiddleware'),
            'aldryn_sites.middleware.SiteMiddleware',
        )

    def security_settings(self, data, settings, env):
        s = settings
        s['SECURE_SSL_REDIRECT'] = env('SECURE_SSL_REDIRECT', False)
        s['SECURE_REDIRECT_EXEMPT'] = env('SECURE_REDIRECT_EXEMPT', [])
        s['SECURE_HSTS_SECONDS'] = env('SECURE_HSTS_SECONDS', 0)
        # SESSION_COOKIE_SECURE is handled by
        #   django.contrib.sessions.middleware.SessionMiddleware
        s['SESSION_COOKIE_SECURE'] = env('SESSION_COOKIE_SECURE', False)
        s['SECURE_PROXY_SSL_HEADER'] = env(
            'SECURE_PROXY_SSL_HEADER',
            ('HTTP_X_FORWARDED_PROTO', 'https')
        )
        # SESSION_COOKIE_HTTPONLY and SECURE_FRAME_DENY must be False for CMS
        # SESSION_COOKIE_HTTPONLY is handled by
        #   django.contrib.sessions.middleware.SessionMiddleware
        s['SESSION_COOKIE_HTTPONLY'] = env('SESSION_COOKIE_HTTPONLY', False)

        s['SECURE_CONTENT_TYPE_NOSNIFF'] = env('SECURE_CONTENT_TYPE_NOSNIFF', False)
        s['SECURE_BROWSER_XSS_FILTER'] = env('SECURE_BROWSER_XSS_FILTER', False)

        s['MIDDLEWARE_CLASSES'].insert(
            s['MIDDLEWARE_CLASSES'].index('aldryn_sites.middleware.SiteMiddleware') + 1,
            'django.middleware.security.SecurityMiddleware'
        )

    def server_settings(self, settings, env):
        settings['PORT'] = env('PORT', 80)
        settings['BACKEND_PORT'] = env('BACKEND_PORT', 8000)
        settings['ENABLE_NGINX'] = env('ENABLE_NGINX', False)
        settings['ENABLE_PAGESPEED'] = env(
            'ENABLE_PAGESPEED',
            env('PAGESPEED', False),
        )
        settings['ENABLE_BROWSERCACHE'] = env(
            'ENABLE_BROWSERCACHE',
            env('BROWSERCACHE', False),
        )
        settings['BROWSERCACHE_MAX_AGE'] = env('BROWSERCACHE_MAX_AGE', 300)
        settings['NGINX_CONF_PATH'] = env('NGINX_CONF_PATH')
        settings['NGINX_PROCFILE_PATH'] = env('NGINX_PROCFILE_PATH')
        settings['PAGESPEED_ADMIN_HTPASSWD_PATH'] = env(
            'PAGESPEED_ADMIN_HTPASSWD_PATH',
            os.path.join(
                os.path.dirname(settings['NGINX_CONF_PATH']),
                'pagespeed_admin.htpasswd',
            )
        )
        settings['PAGESPEED_ADMIN_USER'] = env('PAGESPEED_ADMIN_USER')
        settings['PAGESPEED_ADMIN_PASSWORD'] = env('PAGESPEED_ADMIN_PASSWORD')
        settings['DJANGO_WEB_WORKERS'] = env('DJANGO_WEB_WORKERS', 3)
        settings['DJANGO_WEB_MAX_REQUESTS'] = env('DJANGO_WEB_MAX_REQUESTS', 500)
        settings['DJANGO_WEB_TIMEOUT'] = env('DJANGO_WEB_TIMEOUT', 120)

    def logging_settings(self, settings, env):
        settings['LOGGING'] = {
            'version': 1,
            'disable_existing_loggers': False,
            'filters': {
                'require_debug_false': {
                    '()': 'django.utils.log.RequireDebugFalse',
                },
                'require_debug_true': {
                    '()': 'django.utils.log.RequireDebugTrue',
                },
            },
            'handlers': {
                'console': {
                    'level': 'INFO',
                    'class': 'logging.StreamHandler',
                    'stream': sys.stdout,
                },
                'null': {
                    'class': 'logging.NullHandler',
                },
            },
            'loggers': {
                '': {
                    'handlers': ['console'],
                    'level': 'INFO',
                },
                'django': {
                    'handlers': ['console'],
                    'level': 'INFO',
                },
                'django.request': {
                    'handlers': ['console'],
                    'level': 'INFO',
                    'propagate': False,
                },
                'aldryn': {
                    'handlers': ['console'],
                    'level': 'INFO',
                },
                'py.warnings': {
                    'handlers': ['console'],
                },
            }
        }

    def sentry_settings(self, settings, env):
        sentry_dsn = env('SENTRY_DSN')

        if sentry_dsn:
            settings['INSTALLED_APPS'].append('raven.contrib.django')
            settings['RAVEN_CONFIG'] = {'dsn': sentry_dsn}
            settings['LOGGING']['handlers']['sentry'] = {
                'level': 'ERROR',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            }

    def cache_settings(self, settings, env):
        import django_cache_url
        cache_url = env('CACHE_URL')
        if cache_url:
            settings['CACHES']['default'] = django_cache_url.parse(cache_url)

    def storage_settings_for_media(self, settings, env):
        import yurl
        from aldryn_django.storage import parse_storage_url
        if env('DEFAULT_STORAGE_DSN'):
            settings['DEFAULT_STORAGE_DSN'] = env('DEFAULT_STORAGE_DSN')
        settings['MEDIA_URL'] = env('MEDIA_URL', '/media/')
        if 'DEFAULT_STORAGE_DSN' in settings:
            settings.update(parse_storage_url(settings['DEFAULT_STORAGE_DSN']))
        settings['MEDIA_URL_IS_ON_OTHER_DOMAIN'] = bool(yurl.URL(settings['MEDIA_URL']).host)
        settings['MEDIA_ROOT'] = env('MEDIA_ROOT', os.path.join(settings['DATA_ROOT'], 'media'))

    def storage_settings_for_static(self, settings, env):
        import yurl
        settings['STATIC_URL'] = env('STATIC_URL', '/static/')
        settings['STATIC_URL_IS_ON_OTHER_DOMAIN'] = bool(yurl.URL(settings['STATIC_URL']).host)
        settings['STATIC_ROOT'] = env(
            'STATIC_ROOT',
            os.path.join(settings['BASE_DIR'], 'static_collected'),
        )
        settings['STATICFILES_DIRS'] = env(
            'STATICFILES_DIRS',
            [os.path.join(settings['BASE_DIR'], 'static'),]
        )

    def i18n_settings(self, data, settings, env):
        settings['ALL_LANGUAGES'] = list(settings['LANGUAGES'])
        settings['ALL_LANGUAGES_DICT'] = dict(settings['ALL_LANGUAGES'])
        languages = json.loads(data['languages'])
        settings['LANGUAGE_CODE'] = languages[0]
        settings['USE_L10N'] = True
        settings['USE_I18N'] = True
        settings['LANGUAGES'] = [
            (code, settings['ALL_LANGUAGES_DICT'][code])
            for code in languages
        ]
        settings['LOCALE_PATHS'] = [
            os.path.join(settings['BASE_DIR'], 'locale'),
        ]

    def time_settings(self, settings, env):
        if env('TIME_ZONE'):
            settings['TIME_ZONE'] = env('TIME_ZONE')

    def migration_settings(self, settings, env):
        settings.setdefault('MIGRATION_COMMANDS', [])
        mcmds = settings['MIGRATION_COMMANDS']

        mcmds.append('CACHE_URL="locmem://" python manage.py createcachetable django_dbcache; exit 0')
        mcmds.append('python manage.py migrate --list --noinput && python manage.py migrate --noinput && python manage.py migrate --list --noinput')
