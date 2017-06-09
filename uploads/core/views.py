# coding=utf-8
from django.shortcuts import render, redirect

from uploads.core.forms import ImageForm


def home(request):
    return render(request, 'core/home.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            inst = form.save()
            return redirect(u'../../media/'+inst.img.name)
    else:
        form = ImageForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })
