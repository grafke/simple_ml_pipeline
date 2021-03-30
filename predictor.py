import json

import keras
import numpy as np

from config import APP_TOPIC, MESSAGES_PATH, LATEST_MODEL, LOGGING

from messaging.brokers import get_broker
from utils.messages_utils import append_message, publish_prediction

import logging.config

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('app')

consumer = None
model = None


def trained_model(path):
    return keras.models.load_model(path)


def is_application_message(msg):
    message = json.loads(msg.value)
    return msg.topic == APP_TOPIC and 'prediction' not in message


def predicted_value(message):
    prediction = model.predict([message])
    logger.info('Predicted class: {} || Data: {}'.format(prediction, message))
    return np.argmax(prediction, axis=-1)[0]


def process_message(msg):
    message = json.loads(msg.value)

    if is_application_message(msg):
        request_id = message['request_id']
        pred = predicted_value(json.loads(message['data']))
        publish_prediction(pred, request_id)

        append_message(message['data'], MESSAGES_PATH)


if __name__ == '__main__':
    model = trained_model(LATEST_MODEL)

    broker = get_broker()
    broker.listen(process_message)
