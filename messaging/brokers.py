from google.cloud import pubsub_v1
from google.api_core import retry
import logging.config

from config import LOGGING, BROKER, KAFKA_HOST, TOPICS, GC_PUBSUB_PROJECT_ID, GC_PUBSUB_SUBSCRIPTION, GC_PUBSUB_TOPIC

from kafka import KafkaProducer, KafkaConsumer

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('app')


class Broker:
    def send(self, message):
        ...

    def listen(self, callback):
        ...


class Google(Broker):

    def __init__(self, project_id, subscription_id, topic, timeout):
        self.project_id = project_id
        self.subscription_id = subscription_id
        self.timeout = timeout
        self.producer = pubsub_v1.PublisherClient()

        self.topic_id = topic
        self.num_messages = 1

    def listen(self, callback):
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(self.project_id, self.subscription_id)

        with subscriber:
            response = subscriber.pull(
                request={"subscription": subscription_path, "max_messages": self.num_messages},
                retry=retry.Retry(deadline=300),
            )

            ack_ids = []
            for received_message in response.received_messages:
                callback(received_message.message.data)
                ack_ids.append(received_message.ack_id)

            # Acknowledges the received messages so they will not be sent again.
            subscriber.acknowledge(
                request={"subscription": subscription_path, "ack_ids": ack_ids}
            )

            logger.info(
                f"Received and acknowledged {len(response.received_messages)} messages from {subscription_path}."
            )

    def send(self, message):
        topic_path = self.producer.topic_path(self.project_id, self.topic_id)
        self.producer.publish(topic_path, message).result()


class Kafka(Broker):
    def __init__(self, host, topics):
        self.topics = topics
        self.host = host
        self.producer = KafkaProducer(bootstrap_servers=self.host)
        self.consumer = KafkaConsumer(bootstrap_servers=self.host)

    def listen(self, callback):
        self.consumer.subscribe(self.topics)
        for msg in self.consumer:
            callback(msg)

    def send(self, message):
        for topic in self.topics:
            self.producer.send(topic, message)
            self.producer.flush()


def get_broker():
    if BROKER == 'kafka':
        return Kafka(KAFKA_HOST, TOPICS)
    if BROKER == 'google':
        return Google(GC_PUBSUB_PROJECT_ID, GC_PUBSUB_SUBSCRIPTION, GC_PUBSUB_TOPIC, 1)
    logger.error('Broker not configured')
    exit(1)
