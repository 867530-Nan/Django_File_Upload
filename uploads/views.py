# binding.pry replica code
# package already imported
# code.interact(local=dict(globals(), **locals()))


from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from .models import Upload, Word

from .models import Upload, URLUpload

from .forms import UploadFileForm, URLUploadFileForm

import os
import magic
import re
import code
import urllib.request

from bs4 import BeautifulSoup
from PyPDF2 import PdfFileReader


class UploadView(generic.ListView):
    template_name = 'upload_form/form.html'
    fields = ('Upload File(s)', 'Enter a URL', 'Sing a Song')
    context_object_name = 'upload_list'

    def get_queryset(self):
        return Upload.objects.all()


class SuccessView(generic.TemplateView):
    model = Upload
    template_name = 'upload_form/success.html'


class FailureView(generic.TemplateView):
    model = Upload
    template_name = 'upload_form/failure.html'


def upload_url(request):
    if request.method == 'POST':
        # code.interact(local=dict(globals(), **locals()))
        form = URLUploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = URLUpload(
                url_upload=request.POST['url_upload'], title=request.POST['title'])
            instance.save()
            urlCheck(request.POST['url_upload'])
            return HttpResponseRedirect('/success/')
        else:
            return HttpResponseRedirect('/failure/')
    else:
        return HttpResponseRedirect('/failure/')


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
    with open(f'media/{file}', 'rb') as text_file:
        pdf = PdfFileReader(text_file)
        if pdf.isEncrypted:
            pdf.decrypt('')
        number_of_pages = pdf.getNumPages()
        for page_number in range(number_of_pages):
            page = pdf.getPage(page_number)
            text = page.extractText()
            Word.count_vectorizer(text)


def convertASCII(file):
    document = open(f'media/{file}', 'rb')
    text = document.read().decode("utf-8")
    Word.count_vectorizer(text)


def finishedAndRemoveFiles():
    path = "media"
    file_list = os.listdir(path)
    for i in file_list:
        os.remove(f'media/{i}')


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def urlCheck(path):
    with urllib.request.urlopen(path) as response:
        stripped = striphtml(response.read().decode("utf-8"))
