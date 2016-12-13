# Django settings for customerselfcare project.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Radix Technical', 'technical@radix.co.ke'),
)

MANAGERS = ADMINS

import sys
sys.path.append('/appussd')
from utilities.secure.core import decrypt
from configs.config import databases
dbname = str(databases['core']['string']).split(':')[1].split('/')[1]
dbuser = str(decrypt(databases['core']['username']))
dbpassword = str(decrypt(databases['core']['password']))
dbhost = str(databases['core']['string']).split(':')[0]
dbport = str(databases['core']['string']).split(':')[1].split('/')[0]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        #'NAME': dbname,
        'NAME': databases['core']['string'],
        'USER': dbuser,
        'PASSWORD': dbpassword,
        #'HOST': dbhost,
        #'PORT': dbport,
        'threaded': True,
    }
}
# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Africa/Nairobi'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'si#e$husajizjz*$%#=h*l-bx3e_+c*bpk5%u*y9%e63vtyez0'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'password_policies.middleware.PasswordChangeMiddleware',
    'axes.middleware.FailedLoginMiddleware',
    'customerservice.middleware.AutoLogout',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.contrib.messages.context_processors.messages',
    'password_policies.context_processors.password_status',
)
ROOT_URLCONF = 'customerselfcare.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'customerselfcare.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    "/appussd/customerselfcare/templates"
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'password_policies',
    'customerservice',
    'audittrail',
    'whitelist',
    'myadmin',
    'axes',
    'packages',
)

#SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

#SERIALIZATION_MODULES = { 'goodjson' : 'common.goodjson' }

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
AXES_LOCKOUT_TEMPLATE = 'locked.html'
AXES_LOGIN_FAILURE_LIMIT = 3
SESSION_COOKIE_AGE = 2 * 60 * 60
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
PASSWORD_HISTORY_COUNT = 4
# Defaults to 60 days.
PASSWORD_DURATION_SECONDS = 24 * 45**3
EMAIL_HOST = '172.23.182.56'
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = 'GUI_Support'
EMAIL_PORT = 25
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL  = 'guisupport@mg.airtel.com'
SERVER_EMAIL    = 'guisupport@mg.airtel.com'
GUI_ADDRESS = 'https://172.23.1.66:7070'
