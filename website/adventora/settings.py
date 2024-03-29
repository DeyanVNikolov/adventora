import os.path
from pathlib import Path
# import load_env from os
from os import getenv
import os
from dotenv import load_dotenv

if not os.getenv("PYTHONANYWHERE_SITE"):
    print("LOCAL ENVIRONMENT")
    load_dotenv()
else:
    print("PYTHONANYWHERE ENVIRONMENT")
    project_folder = os.path.expanduser('~/adventora')
    load_dotenv(os.path.join(project_folder, '.env'))

DEBUG = False if os.getenv("PYTHONANYWHERE_SITE") else True

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")


ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'dev.adventora.net',
    'adventora.net',
    'deyanvnikolov.eu.pythonanywhere.com'
]

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'https://dev.adventora.net',
    'https://adventora.net',
    'https://deyanvnikolov.eu.pythonanywhere.com'
]

CSRF_COOKIE_PATH = '/'
CSRF_COOKIE_SECURE = True

TURNSTILE_SITEKEY = os.getenv("TURNSTILE_SITE")
TURNSTILE_SECRET = os.getenv("TURNSTILE_SECRET")

INSTALLED_APPS = [
    'management',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_countries',
    'rest_framework',
    'turnstile',
    'captcha',
    "phonenumber_field",
    'crispy_forms',
    'crispy_bulma',
    'home',
    'authentication',
    'hotel',
    'promocode',
    'social_django',
    'location_field.apps.DefaultConfig',
    'multiselectfield',
    'ckeditor',
    'corsheaders',
    'sri',
    'fontawesomefree',
]

SOCIAL_AUTH_PIPELINE = (

    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'authentication.pipeline.enable_two_factor',
    'authentication.pipeline.send_welcome_email',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'restrictedsessions.middleware.RestrictedSessionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'adventora.middleware.CheckRole',

]

TURNSTILE_DEFAULT_CONFIG = {

    'callback': 'processturn',
    'render': 'explicit',
    'theme': 'dark',

}

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# 1 hour
SESSION_COOKIE_AGE = 60 * 60 * 3

LANGUAGE_COOKIE_NAME = 'lang'
LANGUAGE_COOKIE_SECURE = True

LANGUAGE_COOKIE_AGE = 60 * 60 * 24 * 365 * 10

INTERNAL_IPS = [
    '127.0.0.1',
]

RESTRICTEDSESSIONS_REDIRECT_VIEW = 'home'

ROOT_URLCONF = 'adventora.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["adventora/templates", "adventora/website/adventora/templates", "adventora/website/home/templates", "adventora/website/authentication/templates", "adventora/website/hotel/templates",
                 "adventora/website/promocode/templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'adventora.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'postgres',
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': '5432',

    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': 'db.sqlite3',
    # }
}

AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.reddit.RedditOAuth2',
    'social_core.backends.spotify.SpotifyOAuth2',
    'social_core.backends.trello.TrelloOAuth',
    'social_core.backends.patreon.PatreonOAuth2',
    'social_core.backends.steam.SteamOpenId',
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.amazon.AmazonOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")

SOCIAL_AUTH_GITHUB_KEY = os.getenv("SOCIAL_AUTH_GITHUB_KEY")
SOCIAL_AUTH_GITHUB_SECRET = os.getenv("SOCIAL_AUTH_GITHUB_SECRET")

SOCIAL_AUTH_REDDIT_KEY = os.getenv("SOCIAL_AUTH_REDDIT_KEY")
SOCIAL_AUTH_REDDIT_SECRET = os.getenv("SOCIAL_AUTH_REDDIT_SECRET")
SOCIAL_AUTH_REDDIT_AUTH_EXTRA_ARGUMENTS = {'duration': 'permanent'}

SOCIAL_AUTH_LOGIN_ERROR_URL = '/authentication/login-error/'

SOCIAL_AUTH_SPOTIFY_KEY = os.getenv("SOCIAL_AUTH_SPOTIFY_KEY")
SOCIAL_AUTH_SPOTIFY_SECRET = os.getenv("SOCIAL_AUTH_SPOTIFY_SECRET")

SOCIAL_AUTH_TRELLO_KEY = os.getenv("SOCIAL_AUTH_TRELLO_KEY")
SOCIAL_AUTH_TRELLO_SECRET = os.getenv("SOCIAL_AUTH_TRELLO_SECRET")

SOCIAL_AUTH_PATREON_KEY = os.getenv("SOCIAL_AUTH_PATREON_KEY")
SOCIAL_AUTH_PATREON_SECRET = os.getenv("SOCIAL_AUTH_PATREON_SECRET")

SOCIAL_AUTH_STEAM_API_KEY = os.getenv("SOCIAL_AUTH_STEAM_API_KEY")
SOCIAL_AUTH_STEAM_EXTRA_DATA = ['player']

SOCIAL_AUTH_VK_OAUTH2_KEY = os.getenv("SOCIAL_AUTH_VK_OAUTH2_KEY")
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.getenv("SOCIAL_AUTH_VK_OAUTH2_SECRET")

SOCIAL_AUTH_AMAZON_KEY = os.getenv("SOCIAL_AUTH_AMAZON_KEY")
SOCIAL_AUTH_AMAZON_SECRET = os.getenv("SOCIAL_AUTH_AMAZON_SECRET")

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_IMMUTABLE_USER_FIELDS = ['email', 'first_name', 'last_name', 'username']
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['id']

SOCIAL_AUTH_USER_MODEL = 'authentication.CustomUser'

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

SOCIAL_AUTH_JSONFIELD_ENABLED = True

CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_ALLOW_NONIMAGE_FILES = False

# DISABLE FILE UPLOAD, ONLY TEXT
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'height': 300,
        'width': 700,
        'allowedContent': False,
        'resize_enabled': True,
        'resize_dir': 'both',
        'startupFocus': False,
        'contentsCss': ['/static/css/custom_ckeditor.css'],
        'toolbar_Custom': [
            ['Format', 'Styles', "Font", "FontSize", 'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', 'SpecialChars', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord','-', 'Find', 'Replace','SelectAll' , '-', 'Undo', 'Redo'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', 'HorizontalRule', 'Table'],
            ['RemoveFormat', "TextColor", "BGColor"],
            ['Maximize', 'ShowBlocks', 'Source', 'Preview', 'Print', '-', 'Templates'],
            ['About']
        ],
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),

    },
}

CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
CAPTCHA_TIMEOUT = 10
CAPTCHA_LENGTH = 5
CAPTCHA_FONT_SIZE = 50
CAPTCHA_MATH_CHALLENGE_OPERATOR = '+'
CAPTCHA_IMAGE_SIZE = (200, 100)

COUNTRIES_FIRST = [
    "BG", "RO", "GR", "SRB", "MK", "TR"
]

JAZZMIN_SETTINGS = {
    "site_title": "Adventora Admin",
    "site_header": "Adventora",
    "site_brand": "Adventora",
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "Adventora",
    "copyright": "Adventora LLC",
    "search_model": ["auth.User", "auth.Group"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "GitHub", "url": "https://github.com/deyanvnikolov/adventora", "new_window": True},
        {"model": "auth.User"},
        {"name": "Website", "url": "/", "new_window": False},
    ],
    "usermenu_links": [
        {"name": "Support", "url": "https://github.com/deyanvnikolov/adventora", "new_window": True},
        {"model": "auth.user"}
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "custom_links": {},
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
}

TIME_ZONE = 'EET'

USE_I18N = True

USE_TZ = True
STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticroot')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = ("bulma",)

CRISPY_TEMPLATE_PACK = "bulma"

AUTH_USER_MODEL = 'authentication.CustomUser'

LOGIN_REDIRECT_URL = 'home'

LOGOUT_REDIRECT_URL = 'home'

LOGIN_URL = 'sign-in'

LOGOUT_URL = 'logout'

if not os.getenv("PYTHONANYWHERE_SITE"):
    GDAL_LIBRARY_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'venv', 'Lib', 'site-packages', 'osgeo', 'gdal304.dll')
    GDAL_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'venv', 'Lib', 'site-packages', 'osgeo', 'data')
    GEOS_LIBRARY_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'venv', 'Lib', 'site-packages', 'osgeo', 'geos_c.dll')

LOCATION_FIELD = {
    'map.provider': 'openstreetmap',
    'search.provider': 'google',
    'provider.openstreetmap.max_zoom': 2,
}

LANGUAGE_CODE = 'bg-bg'

LANGUAGES = (
    ('bg', 'Bulgarian'),
    ('en', 'English'),
    ('ro', 'Romanian'),
    ('de', 'German'),
    ('el', 'Greek'),
    ('fi', 'Finnish'),
    ('hu', 'Hungarian'),
    ('hr', 'Croatian'),
    ('sr', 'Serbian'),
    ('no', 'Norwegian'),
    ('sv', 'Swedish'),
    ('ru', 'Russian'),
    ('uk', 'Ukrainian'),
    ('fr', 'French'),
    ('es', 'Spanish'),
    ('it', 'Italian'),
    ('pt', 'Portuguese'),
    ('tr', 'Turkish'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
