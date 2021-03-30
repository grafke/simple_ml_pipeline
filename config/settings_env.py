from pathlib import Path

KAFKA_HOST = '192.168.0.101:9092'
APP_TOPIC = 'app_messages'
TOPICS = [APP_TOPIC]

GC_PUBSUB_PROJECT_ID = ''
GC_PUBSUB_TOPIC = ''
GC_PUBSUB_SUBSCRIPTION = ''

BROKER = 'kafka'  # google | kafka

PATH = Path('resources/')
DATA_PATH = PATH / 'data'
MODELS_PATH = PATH / 'models'
MESSAGES_PATH = PATH / 'messages'
LATEST_MODEL = MODELS_PATH / 'latest.model'

RETRAIN_EVERY = 25
EXTRA_MODELS_TO_KEEP = 1

TF_XLA_FLAGS = '--tf_xla_enable_xla_devices'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'

        },
    },
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'loggers': {
        'app': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    },
}
