import json
import uuid
from time import sleep

from messaging.brokers import get_broker
from utils import mnist_reader

from config import LOGGING, DATA_PATH
import logging.config

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('app')

x_test, y_test = mnist_reader.load_mnist(DATA_PATH, kind='t10k')
messages = x_test


def start_producing():
    broker = get_broker()
    for m in messages:
        message_id = str(uuid.uuid4())
        message = {'request_id': message_id, 'data': json.dumps(m.tolist())}

        broker.send(json.dumps(message).encode('utf-8'))
        logger.info("\033[1;31;40m -- PRODUCER: Sent message with id {}".format(message_id))
        sleep(1)


if __name__ == '__main__':
    start_producing()
