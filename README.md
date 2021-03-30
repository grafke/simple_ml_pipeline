**Requirements**

```
pip install -r requirements.txt
```

**OFFLINE TRAINING (HW Part 1)**

The offline process is fairly standard and all accomplished by running the `initialize.py` script. This script will download the dataset, set the dir structure, pre-preprocess the data, and train an initial model on the training dataset. The results will be saved to disk and from there in advance we are ready to move to the online stage of the process.


**ONLINE PREDICTIONS (HW Part 3)**

 0. The App/Service (`app.py`) will send messages (JSON) into the pipeline. These will be processed and App/Service will then get the results of the predictions.
 1. a) The messages from App/Service will be published to Kafka and, eventualy, received by the Predictor (`predictor.py`)

 	b) The Predictor will process the data and run the algorithm publishing the message with the prediction result back to Kafka, which will be eventually received by App/Service

## How to run the pipeline (with kafka on Mac OS)

1. Start Zookeeper and Kafka. Assuming these are installed using Homebrew, starting these services is as easy as:
```
$ brew services start zookeeper
==> Successfully started `zookeeper` (label: homebrew.mxcl.zookeeper)
$ brew services start kafka
==> Successfully started `kafka` (label: homebrew.mxcl.kafka)
```

Make sure to update the config/settings_env.py

#### Option 1
2. Run docker compose. It will start the producer and consumer apps.
```
docker-compose up
```

2. In Terminal run the Predictor App:
```
python predictor.py
```

#### Option 2
1. In Terminal#1 run the Predictor App:
```
python predictor.py
```

2. In Terminal#2 run the Producer App
```
python producer.py
```

3. In Terminal#3 run the Consumer App
```
python consumer.py
```