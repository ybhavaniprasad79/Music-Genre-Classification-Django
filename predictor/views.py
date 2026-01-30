from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from .apps import PredictorConfig
from .forms import DocumentForm
from .models import Document
from .Metadata import getmetadata
import warnings
from .predict import predict_gen
from django.contrib import messages
warnings.simplefilter('ignore')

class IndexView(TemplateView):
    template_name = 'music/index.html'

def model_form_upload(request):
    import tempfile
    import os
    from django.conf import settings

    documents = Document.objects.all()
    if request.method == 'POST':
        if len(request.FILES) == 0:
            messages.error(request,'Upload a file')
            return redirect("predictor:index")

        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            uploadfile = request.FILES['document']
            print(f"File: {uploadfile.name}, Size: {uploadfile.size}")
            
            if not uploadfile.name.endswith('.wav'):
                messages.error(request,'Only .wav file type is allowed')
                return redirect("predictor:index")
            
            try:
                # Save uploaded file to temp location for librosa to process
                temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
                os.makedirs(temp_dir, exist_ok=True)
                
                temp_file_path = os.path.join(temp_dir, uploadfile.name)
                with open(temp_file_path, 'wb+') as destination:
                    for chunk in uploadfile.chunks():
                        destination.write(chunk)
                
                print(f"Temp file saved: {temp_file_path}")
                meta = getmetadata(temp_file_path)
                print(f"Metadata extracted: {len(meta)} features")
                
                genre = predict_gen(meta)
                print(f"Predicted genre: {genre}")
                
                # Clean up temp file
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

                context = {'genre':genre}
                return render(request,'music/result.html',context)
            
            except Exception as e:
                print(f"Error processing file: {str(e)}")
                import traceback
                traceback.print_exc()
                messages.error(request, f'Error processing file: {str(e)}')
                return redirect("predictor:index")

    else:
        form = DocumentForm()

    return render(request,'music/result.html',{'documents':documents,'form':form})