import datetime
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from seed.models import CustomUser,Grower,Country,City,State,Crop
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import keras
from PIL import Image
import numpy as np  
from keras.models import load_model
from keras.preprocessing import image
import tensorflow as tf
import json
from tensorflow import Graph
# , Session
from django.template.loader import render_to_string
from django.http import HttpResponse
from io import BytesIO
from datetime import date
import pdfkit
import json
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import render
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from django.template.loader import render_to_string
# from weasyprint import HTML
import tempfile
from django.db.models import Sum
from django.http import FileResponse
import io
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import inch
# from reportlab.lib.pagesizes import letter
from xhtml2pdf import pisa
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.template.loader import get_template
from django.template import Context
from io import BytesIO
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa



img_height ,img_width = 224,224

# model = load_model('./models/vgg16AugData.h5')

def Home(request):
    return render(request,'grower/home.html')

def about(request):  
    return render(request, 'grower/about.html')

def contact(request):  
    return render(request, 'grower/contact.html')
    
@login_required(login_url='/')
def add_details(request):
    try:
        user = CustomUser.objects.get(id=request.user.id)
        grower = Grower.objects.get(admin=request.user.id)
        countries = Country.objects.all()
        states = State.objects.all()
        cities = City.objects.all()
        crops = Crop.objects.all()

        # print(grower.country_id)
        # print(grower.city_id)

        context = {
            "grower": grower,
            "user":user,
            "countries": countries,
            "states": states,
            "cities": cities,
            "crops": crops,
            "grower_id": grower.id,
        }
        # print(grower.state_id)

        return render(request, 'grower/add_details.html', context)
    except Grower.DoesNotExist:
        return render(request, 'grower/add_details.html', {})

def update_details(request):
    if request.method == 'POST':
        grower_id = request.POST['grower_id']
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        aadhar_number = request.POST['aadhar_number']
        pan_number = request.POST['pan_number']
        mobile_number = request.POST['mobile_number']
        address = request.POST['address']
        country_id = request.POST['country_id']
        state_id = request.POST['state_id']
        city_id = request.POST['city_id']
        crop_id = request.POST['crop_id']

        grower = Grower.objects.get(id=grower_id)
        grower.admin.first_name = first_name
        grower.admin.last_name = last_name
        grower.admin.email = email
        grower.aadhar_number = aadhar_number
        grower.pan_number = pan_number
        grower.mobile_number = mobile_number
        grower.address = address
        
        country = Country.objects.get(id=country_id)
        grower.country_id = country

        # Similarly, fetch and assign the state, city, and crop instances
        state = State.objects.get(id=state_id)
        grower.state_id = state

        city = City.objects.get(id=city_id)
        grower.city_id = city

        crop = Crop.objects.get(id=crop_id)
        grower.crop_id = crop

        if profile_pic:
            grower.admin.profile_pic = profile_pic

        grower.admin.save()
        grower.save()

        return redirect("testing_page")

    else:
        grower_id = request.GET.get('grower_id')
        grower = Grower.objects.get(id=grower_id)
        countries = Country.objects.all()
        states = State.objects.all()
        cities = City.objects.all()
        crops = Crop.objects.all()

        context = {
            'grower_id': grower_id,
            'grower': grower,
            'countries': countries,
            'states': states,
            'cities': cities,
            'crops': crops,
        }

        return render(request, 'update_details.html', context)

def testing_page(request): 
    grower = Grower.objects.filter(id = request.user.id)
    
    # print(grower.examination_image)
    context = {
            'grower':grower,
        }
    return render(request,'grower/testing_page.html',context)
  
def image_classification(file_path):
    model = keras.models.load_model('models/seeds_cnn_new_.h5')
    # print(model)
    import numpy as np
    # Load and preprocess the image
    # img = image.open(file_path)
    # img_d = img.resize((256, 256))
    img_d = image.load_img(file_path, target_size=(256, 256))

    # if len(np.array(img_d).shape)<4:
    #     rgb_img = image.new("RGB",img_d.size)
    #     rgb_img.paste(img_d)
    # else:
    rgb_img = img_d

    rgb_img = np.array(rgb_img, dtype = np.float64)
    rgb_img = rgb_img.reshape(1,256,256,3)

    predictions = model.predict(rgb_img)
    a= int(np.argmax(predictions))
    print("a is :" ,a)

    if a==0:
        a = 'Average'
    elif a==1:
        a = 'Bad'
    elif a==2:
        a = 'Excellent'
    elif a==3:
        a = 'Good'
    else:
        a = 'Worst' #avergae
    return a
    # print("file path1",file_path)
    # model = keras.models.load_model('models/seeds_cnn_new_.h5')
    # # print(model)
    # import numpy as np
    # # Load and preprocess the image
    # img = image.open(file_path)
    # img = img.resize((256, 256))
    # # img = image.load_img(file_path, target_size=(256, 256))
    # img = image.img_to_array(img)
    # img = np.expand_dims(img, axis=0)
    # img = tf.keras.applications.resnet50.preprocess_input(img)

    # # Make predictions
    # predictions = model.predict(img)
    # class_index = np.argmax(predictions)
    # class_labels = ['Average', 'Class 2', 'Class 3', 'Class 4', 'Class 5']

    # class_label = class_labels[class_index]

    # return class_label
   
def predictImage(request):
    if request.method == 'POST':
        image_file = request.FILES.get('examination_image')
        examination_image = request.FILES.get('examination_image')
        print(image_file)

        grower = Grower.objects.get(admin=request.user.id)
        grower.examination_image = examination_image
        print(grower.examination_image)
        grower.save()
        # if request.method == 'POST':
        fileObj = request.FILES["examination_image"]
        fs = FileSystemStorage()
        filePathName = fs.save(fileObj.name, fileObj)
        filePathName=fs.url(filePathName)

        file_path = os.path.join(settings.MEDIA_ROOT, 'temp', image_file.name)
        print("file path",file_path)
        default_storage.save(file_path, image_file)

        classification_result = image_classification(file_path)
        request.session['classification_result'] = classification_result

        print("the classification result is  :",classification_result)
        default_storage.delete(file_path)

        

        context = {
            'filePathName':filePathName,
            'classification_result': classification_result,
            # 'current_date':current_date,
        }

        return render(request, 'grower/result.html', context)

    return render(request, 'grower/testing_page.html',context)

# def export_pdf(request, classification_result):
#     user = CustomUser.objects.get(id=request.user.id)
#     grower = Grower.objects.get(admin=request.user.id)
        
#     classification_result = request.session.get('classification_result')

#     # Generate the PDF
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="classification_results.pdf"'

#     buffer = BytesIO()

#     p = canvas.Canvas(buffer)

#     p.setFont("Helvetica", 12)
#     # p.drawString(100, 650, "This is the results")
#     p.drawString(250, 750, "CERTIFICATE")
#     # p.drawString(100, 765, "This is to certify that ")
#     p.drawString(100, 725, "This is to certify that the seeds given for testing by Grower :{}".format(user.first_name + " "+user.last_name))
#     p.drawString(100, 710, "are found to be Classification Results are: {}".format(classification_result))

#     p.showPage()
#     p.save()

#     pdf = buffer.getvalue()
#     buffer.close()
#     response.write(pdf)

#     return response

from django.template.loader import render_to_string

def export_pdf(request, classification_result):
    user = CustomUser.objects.get(id=request.user.id)
    grower = Grower.objects.get(admin=request.user.id)
    
    classification_result = request.session.get('classification_result')
    current_date = date.today().strftime("%B %d, %Y")
    
    # p.drawString(400, 750, f"Date: {current_date}")
    
    # Render the certificate HTML template with the necessary data
    context = {
        'user': user,
        'grower': grower,
        'current_date':current_date,
        'classification_result': classification_result
    }
    template = get_template('grower/certificate.html')
    html = template.render(context)
    
    # Generate the PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="classification_results.pdf"'
    
    # Generate PDF using xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        # Handle error
        return HttpResponse('Error generating PDF', status=500)
    
    return response
