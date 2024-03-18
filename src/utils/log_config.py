import logging.config

from src.utils.settings import settings

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': settings.log_level.name,
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['default'],
        'level': settings.log_level.name,
    },
    'loggers': {
        'hypercorn': {
            'level': 'ERROR',
        },
        'asyncio': {
            'level': 'ERROR',
        },
        'httpx': {
            'level': 'ERROR',
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
