import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'ckeditor_uploader',
    'store',
]

# Jazzmin Admin Configuration (optional - can be in settings.py)
JAZZMIN_SETTINGS = {
    "site_title": "Mayaj Admin",
    "site_header": "Mayaj Administration",
    "site_brand": "Mayaj Administration",
    "show_sidebar": True,
    "site_logo": None,
    "login_logo": None,
    "copyright": "MiFa",
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    'hide_models': ['auth.group', 'auth.user','store.ComboProduct','store.ProductImage'],
    "related_modal_active": True,
    'order_with_respect_to': [
        'store',
        # Models
        'store.Order',
        'store.SiteSettings',
        'store.HeroSection',
        'store.RotatingShowcaseProduct',
        'store.Category',
        'store.Product',
        'store.ProductSize',
        'store.ProductReview',
        'store.Offer',
        'store.ComboOffer',
        'store.AboutSection',
        'store.TeamMember',
        'store.ReturnsPageSettings',
        'store.PolicyPoint',
        'store.ReturnStep',
        'store.EligibilityItem',
        'store.RefundMethod',
        'store.ReturnReason',
        'store.ReturnRequest',
        'store.ContactPageSettings',
        'store.ContactInfo',
        'store.ContactMessage',
        'store.ContactFormField',
        'store.BusinessHours',
        'store.SocialMedia',
    ],
    "icons": {
        # Site Configuration
        "store.SiteSettings": "fas fa-cog",
        "store.HeroSection": "fas fa-images",
        
        # Products & Categories
        "store.Category": "fas fa-tags",
        "store.Product": "fas fa-shoe-prints",
        "store.ProductImage": "fas fa-image",
        "store.ProductSize": "fas fa-ruler",
        "store.ProductReview": "fas fa-star",
        "store.RotatingShowcaseProduct": "fas fa-sync",
        
        # Offers & Combos
        "store.Offer": "fas fa-percent",
        "store.ComboOffer": "fas fa-gift",
        "store.ComboProduct": "fas fa-box",
        
        # About & Team
        "store.AboutSection": "fas fa-info-circle",
        "store.TeamMember": "fas fa-users",
        "store.SocialMediaLink": "fas fa-share-alt",
        
        # Returns & Policies
        "store.ReturnsPageSettings": "fas fa-exchange-alt",
        "store.PolicyPoint": "fas fa-list-check",
        "store.ReturnStep": "fas fa-steps",
        "store.EligibilityItem": "fas fa-check-circle",
        "store.RefundMethod": "fas fa-money-bill-wave",
        "store.Notice": "fas fa-exclamation-circle",
        "store.ReturnReason": "fas fa-question-circle",
        "store.ReturnRequest": "fas fa-undo",
        
        # Contact & Support
        "store.ContactPageSettings": "fas fa-address-card",
        "store.ContactInfo": "fas fa-phone",
        "store.SocialMedia": "fas fa-hashtag",
        "store.ContactMessage": "fas fa-envelope",
        "store.ContactFormField": "fas fa-input",
        "store.BusinessHours": "fas fa-clock",
    }
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-indigo",
    "accent": "accent-primary",
    "navbar": "navbar-indigo navbar-dark",
    "no_navbar_border": False,
    "sidebar": "sidebar-dark-indigo",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mayaj.urls'

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

WSGI_APPLICATION = 'mayaj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# Static files (CSS, JavaScript, etc.)
STATIC_URL = '/static/'

# Folders where you store static files 
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  

# Folder where static files will be collected (by collectstatic)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  
# Media files (user uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CKEditor settings
CKEDITOR_UPLOAD_PATH = "uploads/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# cart session id define
CART_SESSION_ID = 'cart'