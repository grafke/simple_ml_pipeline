import json

from config import LOGGING
import logging.config

from messaging.brokers import get_broker

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('app')


def do_something(msg):
    message = json.loads(msg.value)
    if 'prediction' in message:
        request_id = message['request_id']
        logger.info(
            "\033[1;32;40m ** CONSUMER: Received prediction {} for request id {}".format(message['prediction'],
                                                                                         request_id))


def start_consuming():
    broker = get_broker()
    broker.listen(do_something)


if __name__ == '__main__':
    start_consuming()
