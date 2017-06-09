from django import forms

from uploads.core.models import ImageFile


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageFile
        fields = ("img",)
