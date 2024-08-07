import datetime
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from seed.models import CustomUser, Grower, Country, City, State, Crop,Agency, Branch,Field_worker
from django.contrib import messages
from datetime import date
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


def Home(request):
    return render(request, 'agency/home.html')

def about(request):  
    return render(request, 'agency/about.html')

def contact(request):  
    return render(request, 'agency/contact.html')


@login_required(login_url='/')
def add_details(request):
    try:
        user = CustomUser.objects.get(id=request.user.id)
        fieldworker = Field_worker.objects.get(admin=request.user.id)
        # countries = Country.objects.all()
        # growers = Grower.objects.all()
        agencies = Agency.objects.all()
        branches = Branch.objects.all()

        context = {
            # "growers":growers,
            "fieldworker": fieldworker,
            "user": user,
            "agencies": agencies,
            "branches": branches,
            # "cities": cities,
            # "crops": crops,
            "fieldworker_id": fieldworker.id,
        }
        # print(grower.state_id)

        return render(request, 'agency/add_details.html', context)
    except Grower.DoesNotExist:
        return render(request, 'agency/add_details.html', {})

def update_details(request):
    if request.method == 'POST':
        fieldworker_id = request.POST['fieldworker_id']
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        gender = request.POST['gender']
        dob = request.POST['dob']
        phone_number = request.POST['phone_number']
        grower = request.POST['grower']
        agency_id = request.POST['agency_id']
        branch_id = request.POST['branch_id']

        fieldworker = Field_worker.objects.get(id=fieldworker_id)
        fieldworker.admin.first_name = first_name
        fieldworker.admin.last_name = last_name
        fieldworker.admin.email = email
        fieldworker.gender = gender
        fieldworker.dob = dob
        fieldworker.phone_number = phone_number
        fieldworker.grower = grower
        
        agency = Agency.objects.get(id = agency_id)
        fieldworker.agency_id = agency
        branch = Branch.objects.get(id = branch_id)
        fieldworker.branch_id = branch

        if profile_pic:
            fieldworker.admin.profile_pic = profile_pic

        fieldworker.admin.save()
        fieldworker.save()

        return redirect("agency_testing_page")  # Redirect to a success page after saving the details

    else:
        fieldworker_id = request.GET.get('fieldworker_id')  # Assuming you pass the grower_id as a query parameter
        fieldworker = Field_worker.objects.get(id=fieldworker_id)
        agency = Agency.objects.all(agency_id=fieldworker.agency_id)
        branch = Branch.objects.filter(branch_id=fieldworker.branch_id)
        
        context = {
            'fieldworker_id': fieldworker_id,
            'branch': branch,
            'agency': agency,
        }

        return render(request, 'agency/update_details.html', context)

def testing_page(request):
    fieldworker = Field_worker.objects.get(admin=request.user.id)
    user = CustomUser.objects.get(id=request.user.id)
    fieldworker = Field_worker.objects.filter(id=request.user.id)
    
    # print(fieldworker.examination_image)
    context = {
        'fieldworker': fieldworker,
        'user':user,
    }
    return render(request, 'agency/testing_page.html', context)


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

    rgb_img = np.array(rgb_img, dtype=np.float64)
    rgb_img = rgb_img.reshape(1, 256, 256, 3)

    predictions = model.predict(rgb_img)
    a = int(np.argmax(predictions))
    print("a is :", a)

    if a == 0:
        a = 'Average'
    elif a == 1:
        a = 'Bad'
    elif a == 2:
        a = 'Excellent'
    elif a == 3:
        a = 'Good'
    else:
        a = 'Worst'  # avergae
    return a
   
from django.shortcuts import get_object_or_404

def predictImage(request):
    if request.method == 'POST':
        # grower_id = request.POST.get('grower_id')
        # # print(grower_id)
        # grower = get_object_or_404(Grower, admin_id=grower_id)
        image_file = request.FILES.get('examination_image')
        examination_image = request.FILES.get('examination_image')
        print(image_file)

        # grower = Grower.objects.get(admin=grower_id)
        # grower.examination_image = examination_image
        # print(grower.examination_image)
        # grower.save()
        # if request.method == 'POST':
        fileObj = request.FILES["examination_image"]
        fs = FileSystemStorage()
        filePathName = fs.save(fileObj.name, fileObj)
        filePathName = fs.url(filePathName)

        file_path = os.path.join(settings.MEDIA_ROOT, 'temp', image_file.name)
        print("file path", file_path)
        default_storage.save(file_path, image_file)

        classification_result = image_classification(file_path)
        request.session['classification_result'] = classification_result

        print("the classification result is  :", classification_result)
        default_storage.delete(file_path)

        context = {
            'filePathName': filePathName,
            'classification_result': classification_result,

            # 'grower_id':grower_id,
        }

        return render(request, 'agency/result.html', context)

    return render(request, 'agency/testing_page.html', context)


def export_pdf(request, classification_result):
    # grower_id = request.POST.get('grower_id')
    user = CustomUser.objects.get(id=request.user.id)
    fieldworker = Field_worker.objects.get(admin=request.user.id)
    # grower = get_object_or_404(Grower, admin=grower_id)
    # print(grower)
    # print(grower_id)
    # user = grower.admin
    # grower_id = request.POST.get('grower_id')
    # grower = Grower.objects.get(id=grower_id)
    
    classification_result = request.session.get('classification_result')
    current_date = date.today().strftime("%B %d, %Y")
    
    # Render the certificate HTML template with the necessary data
    context = {
        'user': user,
        # 'grower': grower,
        'classification_result': classification_result,
        "fieldworker":fieldworker,
        "current_date":current_date,
    }
    template = get_template('agency/certificate.html')
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


# def update_details(request):
#     if request.method == "POST":
#         # selected_value = request.POST.get('my_dropdown')
#         grower_id = request.POST.get('grower_id')
#         profile_pic = request.FILES.get('profile_pic')
#         # examination_image = request.FILES.get('examination_image')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         # global email
#         email = request.POST.get('email')
#         # username = request.POST.get('username')
#         # password = request.POST.get('password')
#         aadhar_number = request.POST['aadhar_number']
#         pan_number = request.POST['pan_number']
#         mobile_number = request.POST['mobile_number']
#         address = request.POST['address']
#         country_id = request.POST.get('country_id')
#         state_id = request.POST.get('state_id')
#         city_id = request.POST.get('city_id')
#         crop_id = request.POST.get('crop_id')
#         print(profile_pic, grower_id)
#         print("address",address)
#         print(request.POST)
#         # grower.aadhar_number,grower.pan_number,grower.mobile_number)

#         try:
#             # id = 
#             user = CustomUser.objects.get(id=grower_id)
#             print("grower_id",grower_id)
#             # grower = user.grower
#             # print(request.user.id)
#             user.first_name = first_name
#             user.last_name = last_name
#             user.email = email


#             if profile_pic!=None and profile_pic!="":
#                 user.profile_pic = profile_pic
#             user.save()

#             grower = Grower.objects.get(admin = grower_id)
#             # print("hey:",request.user.id)
#             print(grower)
#             grower.address = address
#             grower.aadhar_number = aadhar_number
#             grower.pan_number = pan_number
#             grower.mobile_number = mobile_number

#             country = Country.objects.get(id = country_id)
#             grower.country_id = country

#             state = State.objects.get(id = state_id)
#             grower.state_id = state
#             city = City.objects.get(id = city_id)
#             grower.city_id = city
#             crop = Crop.objects.get(id = crop_id)
#             grower.crop_id = crop

#             grower.save()
#             messages.success(request, "Record Successfully Updated !")

#             return redirect("testing_page")
#         except:
#             messages.error(request,"Failed to Update Your Profile!")

#     return render(request,'agency/testing_page.html')

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

