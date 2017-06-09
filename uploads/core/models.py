from __future__ import unicode_literals

from django.db import models


class ImageFile(models.Model):
    description = models.CharField(max_length=255, blank=True)
    img = models.ImageField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        a=12
        super(ImageFile, self).save(force_insert, force_update, using, update_fields)
        pass
        # from showattendtell import test
        # test.main()
        #
        # if self.pk is not None:  # update
        #     if not self.isReviewed:  # isReviewed = false
        #         self.isReviewed = True
        #
        # if self.pk is None:  # first time upload, run the network for classification
        #     self.imagefile.save(self.imagefile.path.split("/")[-1], self.imagefile.file, False)  # saves the image to file
        #     print "lock status : " + str(lock.locked())  # print lock status
        #     with lock:  # critical section, run the network only 1 at a time
        #         network_cls = subprocess.check_output(["th", "/root/fb.resnet.torch/pretrained/classify_top1.lua",
        #                                                get_active_network_path(),
        #                                                self.imagefile.path])  # call the network to classify the image
        #     # network_cls = "7900300100"
        #     print "classification: "  # write to stdout for debugging
        #     print "old id: " + str(self.plant_id_id)
        #     print "new id: " + network_cls
        #     self.plant_id_id = int(network_cls)  # change plant id to save the network's output
        #
        # super(PlantImage, self).save(force_insert, force_update, using, update_fields)