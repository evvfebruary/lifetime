from torchvision import models
import torch
from pathlib import Path
import numpy as np
from sklearn import svm, metrics, datasets
from sklearn.utils import Bunch
from sklearn.model_selection import GridSearchCV, train_test_split

from skimage.io import imread
import skimage.io
from skimage.transform import resize
import pickle, requests, os
from sklearn.svm import OneClassSVM

from PIL import Image
from torchvision import transforms

from fastai.vision import *
from fastai.metrics import error_rate  # 1 - accuracy
from collections import Counter


def summarize_user_interests(user_photos_urls,
                             user_photos_path='/home/jupyter-vkcracker/researches/data/test_path/',
                             path_to_model='/home/jupyter-vkcracker/researches/model',
                             path_to_detector='/home/jupyter-vkcracker/researches/detector'):
    urls_written = []

    for url in user_photos_urls:
        if not os.path.exists(user_photos_path):
            os.makedirs(user_photos_path)
        r = requests.get(url)

        with open(user_photos_path + url.split('/')[-1], 'wb') as f:
            f.write(r.content)
            urls_written.append(url)

    with open(path_to_model, 'rb') as f:
        learn = pickle.load(f)

    with open(path_to_detector, 'rb') as f:
        outlier_detector = pickle.load(f)

    photo_predictions = {}
    classes = ['diving', 'skiing']

    for url in urls_written:
        img_path = user_photos_path + url.split('/')[-1]
        torch_img = open_image(img_path)
        sklearn_img = skimage.io.imread(img_path)
        img_resized = resize(sklearn_img, (64, 64), anti_aliasing=True, mode='reflect')
        if outlier_detector.predict([img_resized.flatten()]) == 1:
            photo_predictions[url] = classes[np.argmax(learn.predict(torch_img)[2])]
        else:
            photo_predictions[url] = 'no category'

    return dict(Counter(photo_predictions.values())), photo_predictions