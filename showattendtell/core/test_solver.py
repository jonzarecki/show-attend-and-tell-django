from PIL import Image
from scipy import ndimage
import cPickle as pickle
import io
import matplotlib.pyplot as plt
import skimage.transform
import tensorflow as tf
from showattendtell.core.vggnet import Vgg19
from showattendtell.core import utils


from showattendtell.resize import resize_image_test
from utils import *

figure_savepath = os.path.join(os.path.dirname(__file__), "caption_figure_images/")


class CaptioningSolver(object):
    def __init__(self, model, test_model=None):
        """
        Required Arguments:
            - model: Show Attend and Tell caption generating model
            - data: Training data; dictionary with the following keys:
                - features: Feature vectors of shape (82783, 196, 512)
                - file_names: Image file names of shape (82783, )
                - captions: Captions of shape (400000, 17) 
                - image_idxs: Indices for mapping caption to image of shape (400000, ) 
                - word_to_idx: Mapping dictionary from word to index
        Optional Arguments:
            - test_model: String; model path for test 
        """

        self.model = model
        self.test_model = test_model

    def test_live(self, img_path=None):
        """
        - img_path: path to the wanted test image
        """

        # build a graph to sample captions
        # features_batch, image_files = sample_coco_minibatch(data, 2)
        with open("showattendtell/data/coco_minibatch_2.pkl", "rb") as f:
            features_batch, image_files = pickle.load(f)

        def get_image_features(image_path):
            g1 = tf.Graph()  ## This is one graph
            with g1.as_default():
                vgg_model_path = 'showattendtell/data/imagenet-vgg-verydeep-19.mat'
                vggnet = Vgg19(vgg_model_path)  # prepare model for feature extraction
                vggnet.build()
                with tf.Session(config=utils.config) as sess:
                    tf.global_variables_initializer().run()
                    image_batch = np.array(
                        map(lambda x: np.array(resize_image_test(Image.open(x))), [image_path])).astype(
                        np.float32)
                    return sess.run(vggnet.features, feed_dict={vggnet.images: image_batch})

        # img_path = "/home/yonatanz/Projects/PycharmProjects/show-attend-and-tell-django/media/flower-purple-lical" \
        #            "-blosso_wcjmaqj.jpg"
        feats = get_image_features(img_path)

        alphas, betas, sampled_captions = self.model.build_sampler(max_len=20)  # (N, max_len, L), (N, max_len)

        config = tf.ConfigProto(allow_soft_placement=True)
        config.gpu_options.allow_growth = True
        with tf.Session(config=config) as sess:
            saver = tf.train.Saver()
            saver.restore(sess, self.test_model)

            feed_dict = {self.model.features: np.concatenate([feats, features_batch])}
            alps, bts, sam_cap = sess.run([alphas, betas, sampled_captions],
                                          feed_dict)  # (N, max_len, L), (N, max_len)
            decoded = decode_captions(sam_cap, self.model.idx_to_word)

            print "Sampled Caption: %s" % decoded[0]

            # Plot original image
            img = ndimage.imread(img_path)
            plt.subplot(4, 5, 1)
            plt.imshow(img)
            plt.axis('off')

            # Plot images with attention weights
            words = decoded[0].split(" ")
            for t in range(len(words)):
                if t > 18:
                    break
                plt.subplot(4, 5, t + 2)
                plt.text(0, 1, '%s(%.2f)' % (words[t], bts[0, t]), color='black', backgroundcolor='white',
                         fontsize=12)
                plt.imshow(img)
                alp_curr = alps[0, t, :].reshape(14, 14)
                alp_img = skimage.transform.pyramid_expand(alp_curr, upscale=16, sigma=20)
                plt.imshow(alp_img, alpha=0.85)
                plt.axis('off')

            # save figure as numpy array
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plt.gcf().clear()
            return (decoded[0], np.array(Image.open(buf)))
