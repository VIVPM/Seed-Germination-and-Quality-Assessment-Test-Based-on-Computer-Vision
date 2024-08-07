from django.shortcuts import render,redirect,HttpResponse
from seed.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from seed.models import Contact,CustomUser, Grower, Country, City, State, Crop,Agency, Branch,Field_worker,Profile
from .helpers import send_forget_password_mail
import json
from django.core.mail import send_mail
from django.conf import settings


def BASE(request):  
    return render(request, 'base.html')

# def contact(request):  
#     return render(request, 'contact.html')

def about(request):  
    return render(request, 'about.html')

# myapp/views.py
from django.shortcuts import render, redirect
# from .models import CustomUser

def ABOUT(request):
    return render(request,"about.html")


def register(request):
    country = Country.objects.all()
    state = State.objects.all()
    city = City.objects.all()
    crop = Crop.objects.all()
    branch = Branch.objects.all()
    agency = Agency.objects.all()
    grower = Grower.objects.all()
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user_type = request.POST['user_type']
        # profile_pic = request.FILES['profile_pic']
        # profile_pic = request.FILES.get('profile_pic')
        print(user_type)

        request.session['username'] = username
        request.session['email'] = email
        request.session['password'] = password
        request.session['user_type'] = user_type

        # user = CustomUser(username=username, email=email, user_type=user_type)
        
        # user.set_password(password)
        # user.save()

        # print("user_type",user.user_type)

        context= {
            'username':username,
            'email' :email,
            'password' : password,
            'user_type':user_type,
            'country': country,
            'state' : state,
            'city' : city,
            'crop' : crop,
            'branch':branch,
            'agency':agency,
            'grower':grower,
        }

        if user_type == '2':
            return render(request, 'fieldworker.html',context) 
        elif user_type == '3':
            return render(request, 'grower.html',context)  # Replace 'success' with your desired success page URL or name
        else:
            return render(request, 'registration.html') 
    else:
        return render(request, 'registration.html')

def profilegrower(request):
    user = CustomUser.objects.all()
    country = Country.objects.all()
    state = State.objects.all()
    city = City.objects.all()
    crop = Crop.objects.all()
    email = request.session.get('email')
    username = request.session.get('username')
    password = request.session.get('password')
    user_type = request.session.get('user_type')

    if request.method =="POST":
        profile_pic = request.FILES.get('profile_pic')
        examination_image = request.FILES.get('examination_image')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        aadhar_number = request.POST.get('aadhar_number')
        pan_number = request.POST.get('pan_number')
        mobile_number = request.POST.get('mobile_number')
        address = request.POST.get('address')
        country_id = request.POST.get('country_id')
        state_id = request.POST.get('state_id')
        city_id = request.POST.get('city_id')
        crop_id = request.POST.get('crop_id')

        if CustomUser.objects.filter(email = email).exists() :
            messages.warning(request,"Email Is Already Taken")
            return redirect('registration.html') 
        if CustomUser.objects.filter(username = username).exists():
            messages.warning(request,"Username Is Already Taken")
            return redirect('registration.html')
        else:
            user = CustomUser(  
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                profile_pic = profile_pic,
                user_type = user_type,
            )
            user.set_password(password)
            user.save()
            profile_obj = Profile.objects.create(user = user )
            profile_obj.save()

            country_id = Country.objects.get(id = country_id)
            state_id = State.objects.get(id = state_id)
            city_id = City.objects.get(id = city_id)
            crop_id = Crop.objects.get(id = crop_id)

            grower = Grower(
                admin = user,
                address=address,
                country_id = country_id,
                state_id = state_id,
                city_id = city_id,
                crop_id = crop_id,
                aadhar_number = aadhar_number,
                pan_number = pan_number,
                mobile_number = mobile_number,
                examination_image= examination_image,
            )
            grower.save()
            messages.success(request, user.first_name +" "+user.last_name + " Is Successfully Added!")
            return redirect('login')

    context = {
        'country': country,
        'state' : state,
        'city' : city,
        'crop' : crop,
        # 'filePathName':filePathName,
    } 

    return render(request, "login.html",context)

def profilefieldworker(request):
    branch = Branch.objects.all()
    agency = Agency.objects.all()
    grower = Grower.objects.all()
    email = request.session.get('email')
    username = request.session.get('username')
    password = request.session.get('password')
    user_type = request.session.get('user_type')

    if request.method == 'POST':
        profile_pic = request.FILES['profile_pic']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        gender = request.POST['gender']
        dob = request.POST['dob']
        phone_number = request.POST['phone_number']
        agency_id = request.POST['agency_id']
        branch_id = request.POST['branch_id']
        grower = request.POST['grower']
        
        # Save the custom user
        if CustomUser.objects.filter(email = email).exists() :
            messages.warning(request,"Email Is Already Taken")
            return redirect('registration.html') 
        if CustomUser.objects.filter(username = username).exists():
            messages.warning(request,"Username Is Already Taken")
            return redirect('registration.html')
        else:
            user = CustomUser(  
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                profile_pic = profile_pic,
                user_type = user_type,
            )
            user.set_password(password)
            user.save()
            profile_obj = Profile.objects.create(user = user )
            profile_obj.save()
            
           
            agency = Agency.objects.get(id=agency_id)
            branch = Branch.objects.get(id=branch_id)
            
            # Save the field worker
            fieldworker = Field_worker(
                admin=user,
                gender=gender,
                dob=dob,
                phone_number=phone_number,
                agency_id=agency,
                branch_id=branch,
                grower=grower
            )
            
            fieldworker.save()
            messages.success(request, user.first_name +" "+user.last_name + " Is Successfully Added!")
           
            return redirect('login')  # Replace 'fieldworkers_list' with your actual URL name for the fieldworker list page
    
    context = {
        'agency': agency,
        'branch': branch
    }

    return render(request, "login.html", context)

def LOGIN(request):
    return render(request, 'login.html')

def doLogin(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request,
                                         username = request.POST.get('email'),
                                         password = request.POST.get('password'))
        
        if user!=None:
            login(request,user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('admin_home')
                # return HttpResponse('This is Admin login panel')
            elif user_type == '2':
                 return  redirect("agency_home")
            elif user_type == '3':
                return  redirect("grower_home")
            else:
                # message
                messages.error(request, 'Email and password are invalid')
                return redirect('login')
            
        else:
            # message
            messages.error(request, 'Email and password are invalid')
            return redirect('login')
        
def doLogout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id = request.user.id)
    # print(user)
    context = {
        "user": user
    }
    return render(request,'profile.html',context)

@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(profile_pic, first_name,last_name,email,password)
        try:
            customuser = CustomUser.objects.get(id = request.user.id)

            customuser.first_name = first_name
            customuser.last_name = last_name
            customuser.email = email
            

            if password!=None and password!="":
                customuser.set_password(password)
            if profile_pic!=None and profile_pic!="":
                customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request,"Your Profile Updated Successfull!")
            return redirect("profile")

        except:
            messages.error(request,"Failed to Update Your Profile!")
            
    return render(request, 'profile.html')

from django.shortcuts import render, redirect
# from .forms import ContactForm

def contact(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        subject = "Contact Form Submission"
        # message = f"First Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
        message = f"First Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}. Thank you for contacting us.\n We will get back to you.\n Have a good day."
        from_email = 'seedtest987@gmail.com'
        # from_email = settings.EMAIL_HOST_USER
        to_email = [email]  # Change this to your desired recipient email address
        try:
            send_mail(subject, message, from_email, to_email, fail_silently=False)
            messages.success(request, "Email sent successfully!")
        except Exception as e:
            messages.error(request, "Failed to send email. Error: " + str(e))

    
        contact = Contact(
            first_name = first_name,
            last_name = last_name,
            email =email,
            phone = phone,
            message = message,
        )
        contact.save()
        messages.success(request, contact.first_name + " Is Successfully Added!")
        
       
        return redirect('contact')

    return render(request, "contact.html")


import uuid
def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            
            if not CustomUser.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('forget-password')
            
            user_obj = CustomUser.objects.get(username = username)
            token = str(uuid.uuid4())
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'An email is sent.')
            return redirect('forget-password')
    
    except Exception as e:
        print(e)
    return render(request , 'forget-password.html')


def ChangePassword(request , token):
    context = {}
    
    try:
        profile_obj = Profile.objects.filter(forget_password_token = token).first()
        context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')
                
            
            if  new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')
                         
            
            user_obj = CustomUser.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('login')
            
    except Exception as e:
        print(e)
    return render(request , 'change-password.html' , context)

