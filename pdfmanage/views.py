import os
import base64
import time
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from base64 import b64decode
from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse, HttpResponseRedirect

# Create your views here.


require_http_methods(['GET'])
def index(request):
    return render(request, 'index.html')


require_http_methods(['GET', 'POST'])
def handle_pdf_file(request):
    if request.method == 'POST':
        pdf64 = request.POST['encoded']
        split_data = pdf64.split(',')[1]
        # decoded from base64 
        bytese = b64decode(split_data, validate=True)
        if bytese[0:4] != b'%PDF':
            raise ValueError('Missing the PDF file signature')
        # taking current time
        currenttime = str(int(time.time()))
        filepath = settings.MEDIA_ROOT
        # create currenttime  as file name in media folder
        completeName = os.path.join(filepath, currenttime+'.pdf')
        # opening the file and write in it
        file1 = open(completeName, 'wb')
        file1.write(bytese)
        file1.close()
        return HttpResponse("FILE UPLOAD SUCCESSFULL")
    
    else:
        return HttpResponseRedirect('index')



def get_list(request):
    # asign a variable for taking all file name
    list_of_the_files = []
    for file in os.listdir(settings.MEDIA_ROOT):
        list_of_the_files.append(file)

    context ={}
    # now all file name is store in context for template.
    context['lists'] = list_of_the_files
    return render(request, 'lists.html', context)


def pdf_view(request, file_name):
    context = {}
    path_with_file_name = settings.MEDIA_ROOT + '/' + file_name
    try:
        data = open( path_with_file_name, 'rb')

        response = FileResponse(data)

        return response
    except FileNotFoundError:
        raise Http404()