import os.path
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
import dotenv
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)


SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_countries',
    'rest_framework',
    'captcha',
    "phonenumber_field",
    'crispy_forms',
    'crispy_bulma',
    'home',
    'authentication',
    'hotel',
    'api',
    'promocode',
    'social_django',
]

SOCIAL_AUTH_JSONFIELD_ENABLED = True

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
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'adventora.middleware.CheckRole'

]

ROOT_URLCONF = 'adventora.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["adventora/templates"],
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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")

SOCIAL_AUTH_GITHUB_KEY = os.environ.get("SOCIAL_AUTH_GITHUB_KEY")
SOCIAL_AUTH_GITHUB_SECRET = os.environ.get("SOCIAL_AUTH_GITHUB_SECRET")

SOCIAL_AUTH_REDDIT_KEY = os.environ.get("SOCIAL_AUTH_REDDIT_KEY")
SOCIAL_AUTH_REDDIT_SECRET = os.environ.get("SOCIAL_AUTH_REDDIT_SECRET")
SOCIAL_AUTH_REDDIT_AUTH_EXTRA_ARGUMENTS = {'duration': 'permanent'}

SOCIAL_AUTH_SPOTIFY_KEY = os.environ.get("SOCIAL_AUTH_SPOTIFY_KEY")
SOCIAL_AUTH_SPOTIFY_SECRET = os.environ.get("SOCIAL_AUTH_SPOTIFY_SECRET")

SOCIAL_AUTH_TRELLO_KEY = os.environ.get("SOCIAL_AUTH_TRELLO_KEY")
SOCIAL_AUTH_TRELLO_SECRET = os.environ.get("SOCIAL_AUTH_TRELLO_SECRET")

SOCIAL_AUTH_PATREON_KEY = os.environ.get("SOCIAL_AUTH_PATREON_KEY")
SOCIAL_AUTH_PATREON_SECRET = os.environ.get("SOCIAL_AUTH_PATREON_SECRET")

SOCIAL_AUTH_STEAM_API_KEY = os.environ.get("SOCIAL_AUTH_STEAM_API_KEY")
SOCIAL_AUTH_STEAM_EXTRA_DATA = ['player']

SOCIAL_AUTH_VK_OAUTH2_KEY = os.environ.get("SOCIAL_AUTH_VK_OAUTH2_KEY")
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.environ.get("SOCIAL_AUTH_VK_OAUTH2_SECRET")

SOCIAL_AUTH_URL_NAMESPACE = 'social'
URL_NAMESPACE = 'social'

SOCIAL_AUTH_IMMUTABLE_USER_FIELDS = ['email', 'first_name', 'last_name', 'username']


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EET'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    "static/",
    os.path.join(BASE_DIR, "static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = ("bulma",)

CRISPY_TEMPLATE_PACK = "bulma"

AUTH_USER_MODEL = 'authentication.CustomUser'

LOGIN_REDIRECT_URL = 'home'

LOGOUT_REDIRECT_URL = 'home'

LOGIN_URL = 'sign-in'

LOGOUT_URL = 'logout'
