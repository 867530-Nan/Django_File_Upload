from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from .models import Upload, Word

from .forms import UploadFileForm

import os
import io
import re
import magic
from PyPDF2 import PdfFileReader


class UploadView(generic.ListView):
    template_name = 'upload_form/form.html'
    context_object_name = 'upload_list'

    def get_queryset(self):
        return Upload.objects.all()


class SuccessView(generic.TemplateView):
    model = Upload
    template_name = 'upload_form/success.html'


class FailureView(generic.TemplateView):
    model = Upload
    template_name = 'upload_form/failure.html'


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = Upload(
                upload=request.FILES['upload'], title=request.POST['title'])
            instance.save()
            checkTypeSendAway()
            return HttpResponseRedirect('/success/')
        else:
            return HttpResponseRedirect('/failure/')
    else:
        return HttpResponseRedirect('/failure/')
    return render(request, 'upload_form/form.html', {'form': form})


def checkTypeSendAway():
    print("checking type")
    path = "media"
    file_list = os.listdir(path)
    for i in file_list:
        file_type = magic.from_file(f'media/{i}').split(", ")
        if file_type[0] == "ASCII text":
            print("ASCII Document Identified")
            convertASCII(i)
        elif file_type[0] == "PDF document":
            print("PDF Document Identified")
            convertPDF(i)
    finishedAndRemoveFiles()


def convertPDF(file):
    with open(f'media/{file}', 'rb') as f:
        pdf = PdfFileReader(f)
        page = pdf.getPage(0)
        print(page.extractText())


def convertASCII(file):
    document = open(f'media/{file}', 'rb')
    text = document.read().decode("utf-8")
    Word.count_vectorizer(text)


def finishedAndRemoveFiles():
    path = "media"
    file_list = os.listdir(path)
    for i in file_list:
        os.remove(f'media/{i}')
