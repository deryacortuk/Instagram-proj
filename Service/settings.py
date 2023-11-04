from pathlib import Path
import os
import dotenv
from celery.schedules import crontab

env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '.env')

dotenv.load_dotenv(env_file)

BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = "django-insecure-7^+8-$b0_qx&j8@2%0@va7r&ys2b8_i6#g*^z=n)!83uz=*32#"


DEBUG = True

# DEBUG =bool(int(os.environ.get('DEBUG',0)))

ALLOWED_HOSTS = ['127.0.0.1','0.0.0.0','web']




INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.sites',
   'django.contrib.sitemaps',
    "Account.apps.AccountConfig",
    "UserHub.apps.UserhubConfig",
    "Product.apps.ProductConfig",
    'crispy_forms',
    "crispy_bootstrap5",
    "corsheaders",
     "Order.apps.OrderConfig",
      "Payment.apps.PaymentConfig",
       "compressor",
       'django_celery_results',
       'django_celery_beat',
      
]
SITE_ID = 1

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
FILE_UPLOAD_PERMISSIONS = 0o644


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.middleware.gzip.GZipMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    #'django.middleware.http.ConditionalGetMiddleware',
]

ROOT_URLCONF = "Service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR,"templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Service.wsgi.application"
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False
CORS_ALLOWED_ORIGINS = [ 'http://localhost:3030',]
CORS_ALLOWED_ORIGIN_REGEXES = ['http://localhost:3030',]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]



# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_REFERRER_POLICY = "same-origin"
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') 
# X_FRAME_OPTIONS = 'SAMEORIGIN'
# SESSION_COOKIE_AGE = 1209600
# SESSION_SAVE_EVERY_REQUEST = True

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql',

        'NAME': os.environ.get("POSTGRES_DB"),

        'USER': os.environ.get("POSTGRES_USER"),

        'PASSWORD':os.environ.get("POSTGRES_PASSWORD"),

        'HOST': 'pgdb',

        'PORT': os.environ.get("POSTGRES_POST"),
        

    }

}

AWS_S3_GZIP = True
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY =os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'

AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_FILE_OVERWRITE=False
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_VERIFY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR,"staticfiles")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR,"static"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',   
    'compressor.finders.CompressorFinder',
)
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTCATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "Account.authentication.EmailAuthBackend",
]
ADMINS = [(os.environ.get('ADMIN'), os.environ.get('DJANGO_SUPERUSER_EMAIL'))]

EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST="smtp.zoho.eu"
EMAIL_USE_SSL = False
EMAIL_PORT = 587
EMAIL_USE_TLS=True
EMAIL_HOST_PASSWORD= os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER= os.environ.get("EMAIL_HOST_USER")


DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

CELERY_BROKER_URL ="redis://redis:6379/0" 
CELERY_RESULT_BACKEND = 'redis://redis:6379' 
CELERY_ALWAYS_EAGER=True
CELERY_ACCEPT_CONTENT =["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER ="json"
CELERY_TIMEZONE = "UTC"
CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True
CELERY_IGNORE_RESULT = False
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
CELERY_TASK_TIME_LIMIT= 30*60
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_TASK_TRACK_STARTED = True
CELERY_ACKS_LATE = True
CELERY_WORKER_SEND_TASK_EVENTS = True
CELERY_TASK_SEND_SENT_EVENT = True
CELERY_TASK_TRACK_STARTED = True
CELERY_RESULT_BACKEND = "django-db"

CELERY_BEAT_SCHEDULE = {
    'update-status-every-hour': {
        'task': 'UserHub.tasks.celery_cron_tasks', 
        'schedule': crontab(hour="*/1"),
    },
}

STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY") 
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY") 
STRIPE_API_VERSION = '2022-11-15'
STRIPE_WEBHOOK_SECRET=os.environ.get("STRIPE_WEBHOOK_SECRET")

REDIS_HOST="redis"
REDIS_PORT=6379
REDIS_DB =1
CACHE_LOCATION="redis://redis:6379"
REDIS_DB_JOBSTORE=1
REDIS_DB_FSM =1

CACHES = {
 "redis": {
 "BACKEND": "redis_cache.RedisCache",
 "LOCATION": CACHE_LOCATION,
 "TIMEOUT": 60, 
 "KEY_PREFIX": "Service",
  'OPTIONS': {
            'DB': 1,           
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            'PICKLE_VERSION': -1,
            "IGNORE_EXCEPTIONS": True,
        },
 },
}
CACHES["default"] = CACHES["redis"]
DJANGO_REDIS_IGNORE_EXCEPTIONS = True
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
CACHE_MIDDLEWARE_ALIAS = "default"
CACHE_MIDDLEWARE_SECONDS = 1209600

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    
        'root': {
            'handlers': ['console', 'log_file'],
            'level': 'INFO',
           
        },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(module)s] %(message)s',
       
        }
    },
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
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'include_html': True,           
            
        },
        'log_file':{
            'level':'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename' :'logs/djangoproject.log',
            'formatter' :'verbose'
        } 
    },
    'loggers': {
        'django': {
            'handlers': ['console','mail_admins'],
            'propagate': True,
            'level':'INFO'
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        }
    }
}