#!/usr/bin/env python

from argparse import ArgumentParser
import json
import os

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from model import get_model

with open('class_indices.json') as f:
    class_indices = {
        v: k for k, v in json.load(f).items()
    }

def predict_file_path(model, file_path):
    pred_datagen = ImageDataGenerator(rescale=1.0 / 255)

    input_directory = os.path.dirname(file_path)
    input_basename = os.path.basename(file_path)

    df = pd.DataFrame.from_records([{"filename": input_basename}])

    pred_generator = pred_datagen.flow_from_dataframe(
        df, input_directory, class_mode="input", target_size=(224, 224)
    )

    res = model.predict_generator(pred_generator)
    return class_indices[np.argmax(res[0])]


def main():
    parser = ArgumentParser()
    parser.add_argument("inpath")
    args = parser.parse_args()

    model = get_model(weights=None)
    model.load_weights("./trained_model.chkpt")

    print(predict_file_path(model, args.inpath))


if __name__ == "__main__":
    main()
