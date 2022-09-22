import os

config = {
    'recall_endpoint': os.environ['RECALL_ENDPOINT'],
    'redis': {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
    },
}
