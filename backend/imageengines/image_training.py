import os
from django.apps import AppConfig
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
import tensorflow as tf
import datetime
import json
from PIL import Image
import tensorflowjs as tfjs


class AppConfigStartUp(AppConfig):
    name = 'imageengines'

    def ready(self):
        initialize()


gpus = None
imageGenerator = None
# imageRoot = os.path.join(os.getcwd(), 'media')
# modelRoot = os.path.join(os.getcwd(), 'model')


def train(name, param):
    # global imageRoot
    imageRoot = os.path.join(os.getcwd(), 'static', 'image', str(param['pk']), str(param['key']))
    modelRoot = os.path.join(os.getcwd(), 'static', 'model', str(param['pk']), str(param['key']))
    print(imageRoot)
    print(modelRoot)
    # class_index = ['butterfly', 'cat', 'chicken', 'cow', 'dog', 'elephant', 'horse', 'sheep', 'spider', 'squirrel']
    class_index = name
    epochs = int(param['epoch'])
    batch = int(param['batch'])
    rate = param['rate']

    train_set = imageGenerator.flow_from_directory(
        os.path.join(imageRoot),
        target_size=(224, 224),
        batch_size=batch,
        subset='training'
    )

    validation_set = imageGenerator.flow_from_directory(
        os.path.join(imageRoot),
        target_size=(224, 224),
        batch_size=batch,
        subset='validation'
    )

    model = Sequential()
    model.add(layers.InputLayer(input_shape=(224, 224, 3)))
    model.add(layers.Conv2D(16, (3, 3), (1, 1), 'same', activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Dropout(rate=0.3))

    model.add(layers.Conv2D(32, (3, 3), (1, 1), 'same', activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Dropout(rate=0.3))

    model.add(layers.Conv2D(64, (3, 3), (1, 1), 'same', activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Dropout(rate=0.3))

    if len(class_index) == 2:
        model.add(layers.Flatten())
        model.add(layers.Dense(512, activation='relu'))
        model.add(layers.Dense(256, activation='relu'))
        model.add(layers.Dense(len(class_index), activation='sigmoid'))

        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['acc'],
        )

    else:
        model.add(layers.Flatten())
        model.add(layers.Dense(512, activation='relu'))
        model.add(layers.Dense(256, activation='relu'))
        model.add(layers.Dense(len(class_index), activation='softmax'))

        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['acc'],
        )

    epochs = epochs
    model.fit(
        train_set,
        epochs=epochs,
        steps_per_epoch=train_set.samples / batch,
        validation_data=validation_set,
        validation_steps=train_set.samples / batch,
    )

    model_file = os.path.join(modelRoot, 'model.h5')
    if not isFolder(modelRoot):
        os.makedirs(modelRoot)
    model.save(model_file)

    current_timestamp = datetime.datetime.now().isoformat() + 'Z'
    metadata = {
        "tfjsVersion": "1.3.1",
        "tmVersion": "2.3.1",
        "packageVersion": "0.8.4",
        "packageName": "@teachablemachine/image",
        "timeStamp": current_timestamp,
        "userMetadata": {},
        "modelName": "tm-my-image-model",
    }

    class_list = []
    for s in class_index:
        class_list.append(s)
    key = "labels"
    metadata[key] = class_list

    with open(os.path.join(modelRoot, 'metadata.json'), 'w') as outfile:
        json.dump(metadata, outfile)

    convert_tfjs_format(modelRoot)


def convert_tfjs_format(model_save_path):
    command = "tensorflowjs_converter --input_format keras --weight_shard_size_bytes 1000000000 " + \
        os.path.join(model_save_path, 'model.h5 ') + model_save_path
    os.system('cmd /c "' + command + '"')


def isFolder(directory):
    if not os.path.exists(directory):
        return False
    else:
        return True


def initialize():
    global gpus
    global imageGenerator

    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            # Currently, memory growth needs to be the same across GPUs
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
                logical_gpus = tf.config.experimental.list_logical_devices(
                    'GPU')
            print(len(gpus), "Physical GPUs,", len(
                logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            # Memory growth must be set before GPUs have been initialized
            print(e)

    os.environ['TF_ENABLE_WINOGRAD_NONFUSED'] = '1'

    imageGenerator = ImageDataGenerator(
        rescale=1. / 255,
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        brightness_range=[.2, .2],
        horizontal_flip=True,
        validation_split=0.1
    )
