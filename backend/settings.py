from pathlib import Path
import os
import dj_database_url
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

#  chave secreta e debug
SECRET_KEY = config("SECRET_KEY", default="insecure-secret")
DEBUG = config("DEBUG", default=False, cast=bool)

# Configuração de hosts permitidos para produção
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1").split(",")

# Adiciona automaticamente o hostname do Render (externo e interno)
if os.environ.get('RENDER'):
    RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    RENDER_INTERNAL_HOSTNAME = os.environ.get('RENDER_INTERNAL_HOSTNAME')
    
    if RENDER_EXTERNAL_HOSTNAME:
        ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    if RENDER_INTERNAL_HOSTNAME:
        ALLOWED_HOSTS.append(RENDER_INTERNAL_HOSTNAME)

# Adiciona domínios customizados
ALLOWED_HOSTS.extend(['.render.com', '.cptec.co.mz', 'www.cptec.co.mz', 'cptec.co.mz']) 

# 📦 Apps
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'submissions',
    'certifications',
]

# ⚙️ Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configurações de segurança para produção
# Não força HTTPS redirect para permitir fallback HTTP se necessário
if not DEBUG:
    # SECURE_SSL_REDIRECT = True  # Desabilitado para permitir HTTP como fallback
    SESSION_COOKIE_SECURE = False  # Permite cookies em HTTP e HTTPS
    CSRF_COOKIE_SECURE = False  # Permite CSRF em HTTP e HTTPS
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    # SECURE_HSTS_SECONDS = 31536000  # Desabilitado para não forçar HTTPS
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = 'DENY'
else:
    # Desenvolvimento: tudo liberado para HTTP
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# 🗄️ Banco de dados
# Suporta DATABASE_URL do Render ou usa SQLite localmente
DATABASE_URL = config("DATABASE_URL", default=None)

if DATABASE_URL:
    # Produção: PostgreSQL via DATABASE_URL
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Desenvolvimento: SQLite local
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# 🔑 Validação de senha
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🌍 Configurações regionais
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'Africa/Maputo'
USE_I18N = True
USE_TZ = True

# 🧱 Arquivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 🖼️ Mídias
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 🌐 CORS (p/ Vue.js)
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:3000,http://127.0.0.1:3000"
).split(",")

# Adiciona automaticamente URLs do Render no CORS (HTTP e HTTPS)
if os.environ.get('RENDER'):
    RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if RENDER_EXTERNAL_HOSTNAME:
        CORS_ALLOWED_ORIGINS.extend([
            f"https://{RENDER_EXTERNAL_HOSTNAME}",
            f"http://{RENDER_EXTERNAL_HOSTNAME}"
        ])

# Adiciona domínios de produção (HTTP e HTTPS para redundância)
CORS_ALLOWED_ORIGINS.extend([
    'https://www.cptec.co.mz',
    'https://cptec.co.mz',
    'http://www.cptec.co.mz',
    'http://cptec.co.mz'
])

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept', 'accept-encoding', 'authorization', 'content-type', 'dnt',
    'origin', 'user-agent', 'x-csrftoken', 'x-requested-with',
]

# Trusted origins para CSRF (HTTP e HTTPS)
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default=""
).split(",") if config("CSRF_TRUSTED_ORIGINS", default="") else []

# Adiciona automaticamente URLs do Render no CSRF (HTTP e HTTPS para fallback)
if os.environ.get('RENDER'):
    RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if RENDER_EXTERNAL_HOSTNAME:
        CSRF_TRUSTED_ORIGINS.extend([
            f"https://{RENDER_EXTERNAL_HOSTNAME}",
            f"http://{RENDER_EXTERNAL_HOSTNAME}"
        ])

# Adiciona domínios de produção (HTTP e HTTPS para redundância)
CSRF_TRUSTED_ORIGINS.extend([
    'https://*.render.com',
    'http://*.render.com',
    'https://www.cptec.co.mz',
    'https://cptec.co.mz',
    'http://www.cptec.co.mz',
    'http://cptec.co.mz'
])

# ⚙️ Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_FILTER_BACKENDS': ['rest_framework.filters.SearchFilter', 'rest_framework.filters.OrderingFilter'],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}

# Logging configurado por ambiente
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING' if DEBUG else 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING' if DEBUG else 'INFO',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console'],
            'level': 'ERROR' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}


ADMIN_SITE_HEADER = 'CPTec Academy Dashboard'
ADMIN_SITE_TITLE = 'CPTec Admin'
ADMIN_INDEX_TITLE = 'Bem-vindo ao Dashboard'
