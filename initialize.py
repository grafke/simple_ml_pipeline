import os

from config import PATH, DATA_PATH, MODELS_PATH, MESSAGES_PATH, TF_XLA_FLAGS, LATEST_MODEL, LOGGING

os.environ['TF_XLA_FLAGS'] = TF_XLA_FLAGS

from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
import matplotlib.pyplot as plt

from utils import mnist_reader
import logging.config

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('app')


def create_folders():
    logger.info("Creating directories")
    PATH.mkdir(exist_ok=True)
    DATA_PATH.mkdir(exist_ok=True)
    MODELS_PATH.mkdir(exist_ok=True)
    MESSAGES_PATH.mkdir(exist_ok=True)


def fashion_mnist_data():
    x_train, y_train = mnist_reader.load_mnist(DATA_PATH, kind='train')
    x_test, y_test = mnist_reader.load_mnist(DATA_PATH, kind='t10k')

    # -- Change type
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    # -- Normalize
    x_train /= 255
    x_test /= 255

    # -- Change results to category one hot
    y_train = to_categorical(y_train, 10)
    y_test = to_categorical(y_test, 10)

    return {'train_data': x_train,
            'train_labels': y_train,
            'test_data': x_test,
            'test_labels': y_test}


def train_model(data):
    model = init_model()
    model_result = model.fit(data.get('train_data'), data.get('train_labels'),
                             epochs=10,
                             batch_size=64,
                             validation_data=(data.get('test_data'), data.get('test_labels')))

    model.save(LATEST_MODEL)

    score = model.evaluate(data.get('test_data'), data.get('test_labels'))
    logger.info(f"Loss: {score[0]}")
    logger.info(f"Accuracy: {score[1]}")

    plot_accuracy(model_result)
    plot_loss(model_result)


def init_model():
    model = Sequential()
    # -- First layer
    model.add(Dense(400, input_shape=(28 * 28,), activation="relu"))
    # -- Second layer
    model.add(Dense(100, input_shape=(400,), activation="relu"))
    # -- Last layer
    model.add(Dense(10, input_shape=(100,), activation="softmax"))
    model.compile(optimizer="sgd", loss="categorical_crossentropy", metrics=["accuracy"])
    model.summary()
    return model


def plot_loss(hist):
    plt.figure()
    plt.plot(hist.history["loss"])
    plt.plot(hist.history['val_loss'])
    plt.title("Model Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend(["Training Data", "Test Data"], loc="upper right")
    plt.savefig(PATH / 'loss.png')


def plot_accuracy(hist):
    plt.figure()
    plt.plot(hist.history["accuracy"])
    plt.plot(hist.history['val_accuracy'])
    plt.title("Model Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend(["Training Data", "Test Data"], loc="lower right")
    plt.savefig(PATH / 'accuracy.png')


if __name__ == '__main__':
    create_folders()
    data = fashion_mnist_data()
    train_model(data)
