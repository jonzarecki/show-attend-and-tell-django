import os

import matplotlib.pyplot as plt
import cPickle as pickle
import tensorflow as tf
from showattendtell.core.test_solver import CaptioningSolver
from showattendtell.core.model import CaptionGenerator
from showattendtell.core.utils import load_coco_data
from showattendtell.core.bleu import evaluate

dir_path = os.path.dirname(os.path.realpath(__file__))

# %matplotlib inline
plt.rcParams['figure.figsize'] = (8.0, 6.0)  # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'


# %load_ext autoreload
# %autoreload 2
def test_model_on_image(img_path):
    with open(os.path.join(dir_path, 'data/train/word_to_idx.pkl'), 'rb') as f:
        word_to_idx = pickle.load(f)
        model = CaptionGenerator(word_to_idx, dim_feature=[196, 512], dim_embed=512,
                                 dim_hidden=1024, n_time_step=16, prev2out=True,
                                 ctx2out=True, alpha_c=1.0, selector=True, dropout=True)
        solver = CaptioningSolver(model, test_model=os.path.join(dir_path, 'model/lstm/model-20'))

        return solver.test_live(img_path)
