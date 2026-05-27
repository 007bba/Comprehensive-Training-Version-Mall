from pathlib import Path
import os
import datetime


def load_env_file(path):
    if not path.exists():
        return
    for raw_line in path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.lower() in ("1", "true", "yes", "on")


def env_list(name, default=None):
    value = os.environ.get(name)
    if not value:
        return default or []
    return [item.strip() for item in value.split(",") if item.strip()]


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_env_file(BASE_DIR / '.env')
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'change-me-for-local-development')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_bool('DJANGO_DEBUG', True)
ALLOWED_HOSTS = env_list('DJANGO_ALLOWED_HOSTS', ['localhost', '127.0.0.1'])
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.basic',
    'apps.goods',
    'apps.order',
    'apps.users',
    'rest_framework',
    'django_filters',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'corsheaders',
    
    'ckeditor',
    'ckeditor_uploader',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'app6.middle.mymiddle.AuthMiddleware1',
    #'app6.middle.mymiddle.AuthMiddleware2'
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ()
CORS_ALLOW_METHODS  = [
     ' DELETE ',
     ' GET ',
     ' OPTIONS ',
     ' PATCH ',
     ' POST ',
     ' PUT ',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

ROOT_URLCONF = 'myshop.urls'
AUTH_USER_MODEL="users.MyUser"
#LOGIN_URL = '/diy_login/'  #这个路径需要根据你网站的实际登陆地址来设置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
            'libraries':{
                'staticfiles': 'django.templatetags.static',
            }
            
        },
    },
]

WSGI_APPLICATION = 'myshop.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DATABASE', 'shop'),
        'USER': os.environ.get('MYSQL_USER', 'root'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD', ''),
        'HOST': os.environ.get('MYSQL_HOST', '127.0.0.1'),
        'PORT': os.environ.get('MYSQL_PORT', '3306'),
        #取消外键约束，否则多对多模型迁移报django.db.utils.IntegrityError: (1215, 'Cannot add foreign key constraint')
            'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
        }
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level':'DEBUG',
        },
    }
}

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False
STATIC_URL = '/static/'
#STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL="/media/"
MEDIA_ROOT=os.path.join(BASE_DIR,"media")

REST_FRAMEWORK = {
    #'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    #'PAGE_SIZE': 5,
    # 过滤器默认后端
    'DEFAULT_FILTER_BACKENDS': (
           'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 全局配置使用自定义的token认证
        #'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',  
        #'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        #'rest_framework.permissions.IsAuthenticated',
    ),
    #'DEFAULT_RENDERER_CLASSES':(
    #    'app8.customrender.CustomRender',
    #)
    #不然会提示 'AutoSchema' object has no attribute 'get_link'
     'DEFAULT_SCHEMA_CLASS':'rest_framework.schemas.coreapi.AutoSchema',
     #'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',


    #'EXCEPTION_HANDLER': 'common.customexception.custom_exception_handler'
}

# DRF扩展缓存时间
REST_FRAMEWORK_EXTENSIONS = {
    # 缓存时间，单位秒
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 10,
    # 缓存存储，与配置文件中的CACHES的键对应。
    'DEFAULT_USE_CACHE': 'default',
}


JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=30000),  # Token 过期时间为一周
    'JWT_AUTH_HEADER_PREFIX': 'JWT',  # Token的头为：JWT XXXXXXXXXXXXXXXXXXXXXX
    'JWT_ALLOW_REFRESH': False,
    #自定义返回认证信息
    'JWT_RESPONSE_PAYLOAD_HANDLER':'common.jwt_utils.jwt_response_payload_handler'
}

AUTHENTICATION_BACKENDS = (
    'apps.users.views.CustomBackend',
)

CACHES={
    'default':{
        'BACKEND':'django.core.cache.backends.db.DatabaseCache',
        'LOCATION':'my_cache_table',
    }
}




CKEDITOR_UPLOAD_PATH='upload/'
CKEDITOR_IMAGE_BACKEND='pillow'
# 富文本编辑器ckeditor配置
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': (
            ['div', 'Source', '-', 'Save', 'NewPage', 'Preview', '-', 'Templates'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Print', 'SpellChecker', 'Scayt'],
            ['Undo', 'Redo', '-', 'Find', 'Replace', '-', 'SelectAll', 'RemoveFormat'],
            ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField'],
            ['Bold', 'Italic', 'Underline', 'Strike', '-', 'Subscript', 'Superscript'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks', '-', 'About', 'pbckcode'],
            ['Blockquote', 'CodeSnippet'],
        ),
        'width': 'auto',
    },
}




#CACHES = {
#    "default": {
#        "BACKEND": "django_redis.cache.RedisCache",
#        "LOCATION": "redis://192.168.77.101:6379",
#        "OPTIONS": {
#            "CLIENT_CLASS": "django_redis.client.DefaultClient",
#            "PASSWORD":"123456",
#        }
#    }
#}

