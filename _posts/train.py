from fastai.vision import *
from fastai.metrics import error_rate
import fastai
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

path = untar_data(URLs.IMAGEWOOF_160)
tfms = get_transforms()
data = ImageDataBunch.from_folder(path, train='train', valid='val', ds_tfms = tfms,size=160)
learner = cnn_learner(data, models.resnet18, metrics=[accuracy, error_rate])

# learner
learner.save('stage-0')
learner.freeze()
learner.fit(3)
learner.save('stage-1')

