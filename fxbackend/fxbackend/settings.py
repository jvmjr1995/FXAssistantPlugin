# fxbackend/settings.py
# Complete Django settings for FXAssistant with all features enabled

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# In production, load this from environment variables
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 
    "django-insecure-39=594^w&yf(tf%5d5utw2u()^a$k#f1e=s)wqo%seh)p0d2&r")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() == 'true'

# Allowed hosts - add your domain in production
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    # Add your production domain here
    # 'your-domain.com',
]

# Application definition
INSTALLED_APPS = [
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps for API functionality
    'rest_framework',           # Django REST Framework core
    'rest_framework.authtoken', # Token-based authentication
    'corsheaders',             # CORS headers for C++ plugin requests
    
    # Our custom apps
    'presets',                 # User preset management
    'recommendations',         # FX template recommendations and imports
    
    # Optional: Add these for production
    # 'django_extensions',     # Useful development tools
    # 'debug_toolbar',         # Debug toolbar for development
]

# Middleware configuration
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',        # Must be at the top for CORS
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Optional: Add for production
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'fxbackend.urls'

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Add custom template directory
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

WSGI_APPLICATION = 'fxbackend.wsgi.application'

# Database configuration
# For development: SQLite (simple, no setup required)
# For production: PostgreSQL (more robust, scalable)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        
        # For production PostgreSQL, uncomment and configure:
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': os.environ.get('DB_NAME', 'fxassistant'),
        # 'USER': os.environ.get('DB_USER', 'fxassistant'),
        # 'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        # 'HOST': os.environ.get('DB_HOST', 'localhost'),
        # 'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# REST Framework configuration
# This configures the API behavior for the C++ plugin communication
REST_FRAMEWORK = {
    # Authentication methods the API accepts
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',    # For C++ plugin API calls
        'rest_framework.authentication.SessionAuthentication', # For web browser access
    ],
    
    # Default permissions (can be overridden per view)
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly', # Read public, write authenticated
    ],
    
    # API response formatting
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',               # JSON for C++ plugin
        'rest_framework.renderers.BrowsableAPIRenderer',       # Web interface for debugging
    ],
    
    # Request parsing (for file uploads)
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',                   # JSON requests
        'rest_framework.parsers.MultiPartParser',              # File uploads
        'rest_framework.parsers.FormParser',                   # Form data
    ],
    
    # Pagination for large result sets
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,  # Default 20 results per page
    
    # Rate limiting (basic protection)
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',          # Anonymous users
        'rest_framework.throttling.UserRateThrottle'           # Authenticated users
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',      # Anonymous: 100 requests/hour
        'user': '1000/hour',     # Authenticated: 1000 requests/hour
    }
}

# CORS settings for C++ plugin communication
# This allows the plugin to make requests from different origins
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",     # React development server (future web interface)
    "http://127.0.0.1:3000",
    "http://localhost:8080",     # Alternative development port
    "http://127.0.0.1:8080",
]

# Allow all origins in development (NEVER use in production)
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True

# Headers that the plugin can send
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',        # For token authentication
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# HTTP methods the plugin can use
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Password validation
# These ensure users create secure passwords
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,  # Minimum 8 characters
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# Configure paths for serving static content
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # For production deployment

STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Additional static files directory
]

# Media files (User uploads)
# This handles file uploads from the preset import feature
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024    # 10MB max file size in memory
DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024    # 50MB max total upload size
FILE_UPLOAD_PERMISSIONS = 0o644                    # File permissions for uploads

# Temporary file handling (for preset imports)
FILE_UPLOAD_TEMP_DIR = BASE_DIR / 'tmp'
if not FILE_UPLOAD_TEMP_DIR.exists():
    FILE_UPLOAD_TEMP_DIR.mkdir()

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging configuration
# This helps with debugging and monitoring
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'recommendations': {  # Our app-specific logging
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'presets': {  # Preset app logging
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}

# Create logs directory if it doesn't exist
LOGS_DIR = BASE_DIR / 'logs'
if not LOGS_DIR.exists():
    LOGS_DIR.mkdir()

# Cache configuration (for better performance)
# In development, use local memory cache
# In production, consider Redis or Memcached
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'fxassistant-cache',
        'TIMEOUT': 300,  # 5 minutes default timeout
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}

# Session configuration
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True

# Security settings (important for production)
if not DEBUG:  # Production security settings
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Add your domain here for production
    ALLOWED_HOSTS = [
        'your-production-domain.com',
        'api.your-domain.com',
    ]

# Email configuration (for user notifications, password resets)
# Configure this for production use
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Development
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'   # Production

# For production SMTP:
# EMAIL_HOST = 'smtp.your-email-provider.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@domain.com'
# EMAIL_HOST_PASSWORD = 'your-email-password'
# DEFAULT_FROM_EMAIL = 'FXAssistant <noreply@your-domain.com>'

# Custom settings for FXAssistant
# These are application-specific configurations

# Template system settings
FXASSISTANT_SETTINGS = {
    # Maximum number of templates per user
    'MAX_USER_TEMPLATES': 1000,
    
    # Maximum FX chain length
    'MAX_FX_CHAIN_LENGTH': 20,
    
    # Import limits
    'MAX_IMPORT_FILES_PER_REQUEST': 100,
    'MAX_IMPORT_FILE_SIZE': 10 * 1024 * 1024,  # 10MB
    'ALLOWED_IMPORT_EXTENSIONS': ['.xml', '.xps', '.ffp', '.json', '.spl', '.fxp', '.fxb'],
    
    # Community features
    'MIN_RATING_FOR_PUBLIC': 3.0,
    'MAX_PUBLIC_TEMPLATES_PER_USER': 50,
    
    # Cache timeouts
    'FACTORY_TEMPLATE_CACHE_TIMEOUT': 3600,  # 1 hour
    'USER_TEMPLATE_CACHE_TIMEOUT': 300,      # 5 minutes
    'COMMUNITY_TEMPLATE_CACHE_TIMEOUT': 900, # 15 minutes
    
    # Legal compliance
    'LEGAL_DISCLAIMER_VERSION': '1.0',
    'EXTRACTION_METHOD': 'structure_only',
    'STORE_COPYRIGHTED_CONTENT': False,
    'STORE_PARAMETER_VALUES': False,
    'STORE_BRAND_NAMES': False,
}

# Development-only settings
if DEBUG:
    # Allow easier debugging
    CORS_ALLOW_ALL_ORIGINS = True
    
    # Show detailed error pages
    INTERNAL_IPS = [
        '127.0.0.1',
        'localhost',
    ]
    
    # Add debug toolbar if installed
    try:
        import debug_toolbar
        INSTALLED_APPS.append('debug_toolbar')
        MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    except ImportError:
        pass

# Production optimizations
if not DEBUG:
    # Database connection pooling
    DATABASES['default']['CONN_MAX_AGE'] = 60
    
    # Static file compression
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
    
    # Cache templates in production
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]),
    ]

# Import local settings (for sensitive production configs)
try:
    from .local_settings import *
except ImportError:
    pass

# Validation
assert SECRET_KEY, "SECRET_KEY must be set"
if not DEBUG:
    assert 'your-production-domain.com' not in ALLOWED_HOSTS, "Update ALLOWED_HOSTS for production"

print(f"Django settings loaded - DEBUG={DEBUG}, ALLOWED_HOSTS={ALLOWED_HOSTS}")