'''
The setup for rabbitmq message broker (we can also user Redis for this)
'''
import os
from kombu import Exchange, Queue, serialization
import djcelery
from {{ project_name }}.utils import make_memcached_cache


# REDIS

SESSION_CACHE_ALIAS = "sessions"
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

REDIS_HOSTNAME = 'localhost'
REDIS_PORT = 6379
REDIS_SERVER = (REDIS_HOSTNAME, REDIS_PORT, 0)  # host, port, db
REDIS_PASSWORD = ''
REDIS_DB = 1  # keep cache entries in a different db so we can clear them easily
REDIS_HOST = os.environ.get('REDIS_PORT_6379_TCP_ADDR', 'redis')


CACHES = {
    "default": {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    "sessions": {
        "BACKEND": "redis_cache.cache.RedisCache",
        "LOCATION": 'redis:6379',
        "OPTIONS": {
            'DB': 10,
        },
        "KEY_PREFIX": "sessions"
    },
    'staticfiles': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': 'redis:6379',
        'TIMEOUT': 86400 * 365,
        'KEY_PREFIX': 'staticfiles',
    },
    'api': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': 'redis:6379',
        'TIMEOUT': 86400 * 365,
        'KEY_PREFIX': 'api',
    },
}


# RABBITMQ
RABBIT_HOSTNAME = os.environ.get('RABBIT_PORT_5672_TCP', 'rabbit')

if RABBIT_HOSTNAME.startswith('tcp://'):
    RABBIT_HOSTNAME = RABBIT_HOSTNAME.split('//')[1]

BROKER_URL = os.environ.get('BROKER_URL', '')
if not BROKER_URL:
    BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}/'.format(
        user=os.environ.get('RABBIT_ENV_USER', 'rabbit_user'),
        password=os.environ.get('RABBIT_ENV_RABBITMQ_PASS', 'rabbit_user_default_pass'),
        hostname=RABBIT_HOSTNAME,
        vhost=os.environ.get('RABBIT_ENV_VHOST', ''))


# We don't want to have dead connections stored on rabbitmq, so we have to negotiate using heartbeats
BROKER_HEARTBEAT = '?heartbeat=30'
if not BROKER_URL.endswith(BROKER_HEARTBEAT):
    BROKER_URL += BROKER_HEARTBEAT

BROKER_POOL_LIMIT = 1
BROKER_CONNECTION_TIMEOUT = 10


# CELERY CONFIGURATION
# CONFIGURE QUEUES, CURRENTLY WE HAVE ONLY ONE
CELERY_CREATE_MISSING_QUEUES = True
CELERY_RESULT_PERSISTENT = True

CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('{{ project_name }}', Exchange('{{ project_name }}'), routing_key='{{ project_name }}'),
)


# SENSIBLE SETTINGS FOR CELERY
CELERY_ALWAYS_EAGER = False
CELERY_ACKS_LATE = True
CELERY_TASK_PUBLISH_RETRY = True
CELERY_DISABLE_RATE_LIMITS = False

# BY DEFAULT WE WILL IGNORE RESULT
# IF YOU WANT TO SEE RESULTS AND TRY OUT TASKS INTERACTIVELY, CHANGE IT TO FALSE
# OR CHANGE THIS SETTING ON TASKS LEVEL
CELERY_IGNORE_RESULT = True
CELERY_SEND_TASK_ERROR_EMAILS = False
CELERY_TASK_RESULT_EXPIRES = 600

# SET REDIS AS CELERY RESULT BACKEND
CELERY_RESULT_BACKEND = 'redis://%s:%d/%d' % (REDIS_HOSTNAME, REDIS_PORT, REDIS_DB)
CELERY_REDIS_MAX_CONNECTIONS = 1

# DON'T USE PICKLE AS SERIALIZER, JSON IS MUCH SAFER
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYD_HIJACK_ROOT_LOGGER = False
CELERYD_PREFETCH_MULTIPLIER = 1
CELERYD_MAX_TASKS_PER_CHILD = 1000


# ACTIVATE SETTINGS
djcelery.setup_loader()
