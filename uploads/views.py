from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic

from .models import Upload

from .forms import UploadFileForm
# Create your views here.


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
            return HttpResponseRedirect('/success/')
        else:
            return HttpResponseRedirect('/failure/')
    else:
        form = UploadFileForm()
    return render(request, 'upload_form/form.html', {'form': form})
