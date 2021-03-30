import json

from kafka import KafkaProducer

from config import KAFKA_HOST, APP_TOPIC

producer = KafkaProducer(bootstrap_servers=KAFKA_HOST)


def publish_prediction(pred, request_id):
    producer.send(APP_TOPIC, json.dumps({'request_id': request_id, 'prediction': float(pred)}).encode('utf-8'))
    producer.flush()


def read_messages_count(path, repeat_every):
    file_list = list(path.iterdir())
    nfiles = len(file_list)
    if nfiles == 0:
        return 0
    else:
        return ((nfiles - 1) * repeat_every) + len(file_list[-1].open().readlines())


def append_message(message, path):
    message_fname = 'messages.txt'
    f = open(path / message_fname, "a")
    f.write("%s\n" % (json.dumps(message)))
    f.close()
