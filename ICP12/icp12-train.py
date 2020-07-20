import numpy, random, sklearn, pandas, math
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from os import path
from tensorflow.keras.layers import BatchNormalization, Conv2D, Dense
from tensorflow.keras.layers import GlobalAveragePooling2D, LeakyReLU
from tensorflow.keras.layers import MaxPooling2D, SpatialDropout2D
from tensorflow.keras.models import Sequential
keras.backend.set_image_data_format("channels_last")

base = "/media/pi/USB DISK/UrbanSound8K";
metadata = pandas.read_csv(path.join(base, "metadata/UrbanSound8K.csv"))
CLASSES = ["air_conditioner", "car_horn", "children_playing",
          "dog_bark", "drilling", "engine_idling", "gun_shot",
          "jackhammer", "siren", "street_music"]

# load data
features = numpy.load("data/features.npy")
labels = numpy.load("data/labels.npy")

# Split into training + validation data sets
class Dataset:
    rows = 40
    columns = 174
    channels = 1
    __onehot = {CLASSES[i]: numpy.array([1 if x == i else 0
                             for x in range(len(CLASSES))])
              for i in range(len(CLASSES))}
    
    def __init__(my, index):
        my.features = numpy.take(features, index, axis = 0)
        my.labels = numpy.take(labels, index, axis = 0)
        my.metadata = metadata.iloc[index]
        
        # one-hot encode
        my.labels = numpy.array(
            [Dataset.__onehot[label] for label in my.labels])
        
        # reshape to match input
        my.features = my.features.reshape(
            my.features.shape[0], Dataset.rows, Dataset.columns,
            Dataset.channels)
        
samples = len(metadata)
indexes = list(range(samples))
random.shuffle(indexes)

split_offset = math.floor(samples * 80 / 100)
training = Dataset(indexes[0:split_offset])
validation = Dataset(indexes[split_offset:samples])

# describe a model
model = Sequential([
    Conv2D(filters = 32, kernel_size = (3, 3),
           kernel_regularizer = keras.regularizers.l2(0.0005),
           input_shape = (Dataset.rows, Dataset.columns, Dataset.channels)),
    LeakyReLU(alpha = 0.1),
    BatchNormalization(),
    SpatialDropout2D(0.07),
    Conv2D(filters = 32, kernel_size = (3, 3),
           kernel_regularizer = keras.regularizers.l2(0.0005)),
    LeakyReLU(alpha = 0.1),
    BatchNormalization(),
    MaxPooling2D(pool_size = (2, 2)),
    SpatialDropout2D(0.07),
    Conv2D(filters = 64, kernel_size = (3, 3),
           kernel_regularizer = keras.regularizers.l2(0.0005)),
    LeakyReLU(alpha = 0.1),
    BatchNormalization(),
    SpatialDropout2D(0.14),
    Conv2D(filters = 64, kernel_size = (3, 3),
           kernel_regularizer = keras.regularizers.l2(0.0005)),
    LeakyReLU(alpha = 0.1),
    BatchNormalization(),
    GlobalAveragePooling2D(),
    Dense(len(CLASSES), activation = "softmax")
])

if path.exists("data/network.hdf5"):
    model = keras.models.load_model("data/network.hdf5")
    
model.summary()
model.compile(optimizer = "adam",
              loss = "categorical_crossentropy",
              metrics = ["accuracy"])

# train the model
checkpointer = keras.callbacks.ModelCheckpoint(
    filepath = "data/network.hdf5", verbose = 1, save_best_only = True)

history = model.fit(training.features, training.labels,
    batch_size = 16,
    epochs = 200,
    validation_split = 1 / 10,
    callbacks = [checkpointer],
    verbose = 1)
