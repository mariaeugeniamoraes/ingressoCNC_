"""
Django settings for config project.
"""

from pathlib import Path
import os

from dotenv import load_dotenv
import dj_database_url


# ========================================
# CAMINHOS DO PROJETO
# ========================================

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')


# ========================================
# SEGURANÇA / AMBIENTE
# ========================================

# No computador, usa a chave do .env.
# No servidor, usaremos uma variável de ambiente.
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-local-development-key'
)

# Localmente continuará True.
# No servidor configuraremos DEBUG=False.
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'


ALLOWED_HOSTS = os.getenv(
    'ALLOWED_HOSTS',
    '127.0.0.1,localhost'
).split(',')


# ========================================
# APLICAÇÕES
# ========================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'ingressos',
]


# ========================================
# MIDDLEWARE
# ========================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Permite servir CSS, JS e imagens em produção
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ========================================
# URLS / TEMPLATES
# ========================================

ROOT_URLCONF = 'config.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'config.wsgi.application'


# ========================================
# BANCO DE DADOS
# ========================================

DATABASE_URL = os.getenv('DATABASE_URL')


if DATABASE_URL:

    # Banco usado quando o projeto estiver publicado
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

else:

    # MySQL usado no seu computador
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',

            'NAME': os.getenv('DB_NAME'),

            'USER': os.getenv('DB_USER'),

            'PASSWORD': os.getenv('DB_PASSWORD'),

            'HOST': os.getenv('DB_HOST'),

            'PORT': os.getenv('DB_PORT'),
        }
    }


# ========================================
# VALIDAÇÃO DE SENHAS
# ========================================

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


# ========================================
# IDIOMA / HORÁRIO
# ========================================

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# ========================================
# ARQUIVOS ESTÁTICOS
# CSS / JAVASCRIPT / IMAGENS
# ========================================

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'


# ========================================
# EMAIL
# ========================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'