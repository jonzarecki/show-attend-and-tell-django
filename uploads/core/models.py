from __future__ import unicode_literals

import cPickle as pickle
import scipy
import subprocess
import threading
from PIL import Image

from django.db import models

lock = threading.Lock()  # resource lock, run only 1 network at a time


class ImageFile(models.Model):
    description = models.CharField(max_length=255, blank=True)
    img = models.ImageField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None:  # first time upload, run the network for tagging
            print "lock status : " + str(lock.locked())  # print lock status
            self.img.save(self.img.path.split("/")[-1], self.img.file, False)  # saves the image to file
            with lock:  # critical section, run the network only 1 at a time
                from showattendtell import test
                caption, img = test.test_model_on_image(self.img.path)
                self.description = caption

        super(ImageFile, self).save(force_insert, force_update, using, update_fields)
        im = Image.fromarray(img)  # change file to attention picture
        im.save(self.img.path)