from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from seed.models import CustomUser,Contact,Country,City,State, Variety,Season ,Crop,Grower,Branch,Agency,Field_worker
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
import json

def contact(request):  
    return render(request, 'admin/contact.html')

def about(request):  
    return render(request, 'admin/about.html') 

@login_required(login_url='/')
def HOME(request):
    grower_count = Grower.objects.all().count()
    # agency_count = A.objects.all().count()
    crop_count = Crop.objects.all().count()
    variety_count = Variety.objects.all().count()

    context = {
        'grower_count' : grower_count,
        'crop_count' : crop_count,
        # 'agency_count':agency_count,
        'variety_count' : variety_count,
    }
    return render(request, 'admin/home.html',context)

@login_required(login_url='/')
def ADD_GROWER(request):
    country = Country.objects.all()
    state = State.objects.all()
    city = City.objects.all()
    crop = Crop.objects.all()

    if request.method =="POST":
        profile_pic = request.FILES.get('profile_pic')
        examination_image = request.FILES.get('examination_image')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
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
            return redirect('add_grower') 
        if CustomUser.objects.filter(username = username).exists():
            messages.warning(request,"Username Is Already Taken")
            return redirect('add_grower')
        else:
            user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                profile_pic = profile_pic,
                user_type = 3,
            )
            user.set_password(password)
            user.save()

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
            return redirect('view_grower')

    context = {
        'country': country,
        'state' : state,
        'city' : city,
        'crop' : crop,
        # 'filePathName':filePathName,
    } 

    return render(request, "admin/add_grower.html",context)

def VIEW_GROWER(request):
    grower = Grower.objects.all()
    # print(grower)

    context = {
        'grower' : grower,
    }
    return render(request,'admin/view_grower.html',context)

from django.views.decorators.csrf import csrf_exempt

# 2. Exempt the view from CSRF checks
@csrf_exempt
def EDIT_GROWER(request,id):
    grower = Grower.objects.filter(id = id)
    # user = CustomUser.objects.filter(admin = id)
    countries = Country.objects.all()
    states = State.objects.all()
    cities = City.objects.all()
    crops = Crop.objects.all()
    # selected_value = grower.country_id

    context = {
        'grower' : grower,
        'countries': countries,
        'states' : states,
        'cities' : cities,
        'crops' : crops,
        # 'user':user,
        # 'selected_value': selected_value,
    }
    return render(request,'admin/edit_grower.html',context)


def UPDATE_GROWER(request):
    if request.method == "POST":
        # selected_value = request.POST.get('my_dropdown')
        grower_id = request.POST.get('grower_id')
        profile_pic = request.FILES.get('profile_pic')
        examination_image= request.FILES.get('examination_image')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        aadhar_number = request.POST.get('aadhar_number')
        pan_number = request.POST.get('pan_number')
        mobile_number = request.POST.get('mobile_number')
        address = request.POST.get('address')
        country_id = request.POST.get('country_id')
        state_id = request.POST.get('state_id')
        city_id = request.POST.get('city_id')
        crop_id = request.POST.get('crop_id')
        print(profile_pic, grower_id)

        user = CustomUser.objects.get(id = grower_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        
        if password!=None and password!="":
            user.set_password(password)
        if profile_pic!=None and profile_pic!="":
            user.profile_pic = profile_pic
        user.save()

        grower = Grower.objects.get(admin = grower_id)
        grower.address = address
        grower.aadhar_number = aadhar_number
        grower.pan_number = pan_number
        grower.mobile_number = mobile_number
        grower.examination_image = examination_image
        
        country = Country.objects.get(id = country_id)
        grower.country_id = country
        state = State.objects.get(id = state_id)
        grower.state_id = state
        city = City.objects.get(id = city_id)
        grower.city_id = city
        crop = Crop.objects.get(id = crop_id)
        grower.crop_id = crop

        grower.save()
        messages.success(request, "Record Successfully Updated !")

        return redirect("view_grower")

    return render(request,'admin/edit_grower.html')

# def DELETE_GROWER(request, admin):
#     grower = CustomUser.objects.get(id = admin)
#     grower.delete()
#     messages.success(request, "Record Is Successfully Deleted!")
#     return redirect("view_grower")


def DELETE_GROWER(request, admin):
    grower = CustomUser.objects.get(id = admin)
    grower.delete()
    messages.success(request, "Record Is Successfully Deleted!")
    return redirect("view_grower")

# season
# @login_required(login_url='/')

def ADD_SEASON(request):
    if request.method == "POST":
        name = request.POST.get('name')
        season_from_date = request.POST.get('season_from_date')
        season_to_date = request.POST.get('season_to_date')
    
        season = Season(
            name = name,
            from_date = season_from_date,
            to_date = season_to_date,
        )
        season.save()
        messages.success(request, season.name + " Is Successfully Added!")
        return redirect('view_season')

    return render(request, "admin/add_season.html")

def VIEW_SEASON(request):
    season = Season.objects.all()
    # print(season)

    context = {
        'season' : season,
    }
    return render(request,'admin/view_season.html',context)

def EDIT_SEASON(request,id):
    season = Season.objects.filter(id = id)
    print(season,id)
    
    context = {
        'season' : season,  
    }
    return render(request,'admin/edit_season.html',context)

def UPDATE_SEASON(request):
    if request.method == "POST":
        season_id = request.POST.get('season_id')
        name = request.POST.get('name')
        season_from_date = request.POST.get('season_from_date')
        season_to_date = request.POST.get('season_to_date')

        season = Season.objects.get(id = season_id)
        season.name = name
        season.from_date = season_from_date
        season.to_date = season_to_date
        
        # season.save()

        # season =Season.objects.get(admin = se ason_id)
        season.save()
        messages.success(request, "Record Successfully Updated !")

        return redirect("view_season")

    return render(request,'admin/view_season.html')

# def DELETE_SEASON(request, id):
#     season = Season.objects.get(id = id)
#     season.delete()
#     messages.success(request, "Record Is Successfully Deleted!")
#     return redirect("view_season")

from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

# 2. Exempt the view from CSRF checks
@csrf_exempt
def DELETE_SEASON(request, id):
    season = Season.objects.get(id=id)
    season.delete()
    messages.success(request, "Record Is Successfully Deleted!")
    return redirect("view_season")

# variety

def ADD_VARIETY(request):
    if request.method =="POST":
        name = request.POST.get('name')
        yield_per_acre = request.POST.get('yield_per_acre')
        description = request.POST.get('description')
        variety_image = request.FILES.get('variety_image')
        maturity_duration = request.POST.get('maturity_duration')
        
        # print(variety_image,first_name,address,country_id, state_id,city_id,email)

        variety = Variety(
            name = name,
            yield_per_acre = yield_per_acre,
            description = description,
            maturity_duration = maturity_duration,
            variety_image = variety_image,
        )
        
        variety.save()

        messages.success(request, variety.name + " Is Successfully Added!")
        return redirect('view_variety')

   

    # return render(request, "admin/add_grower.html",context)
    return render(request, "admin/add_variety.html")


def VIEW_VARIETY(request):
    variety = Variety.objects.all()
    # print(season)

    context = {
        'variety' : variety,
    }
    return render(request,'admin/view_variety.html',context)


def EDIT_VARIETY(request, id):
    variety = Variety.objects.filter(id = id)
    print(variety)
    
    context = {
        'variety' : variety,
    }
    return render(request,'admin/edit_variety.html',context)
  
def UPDATE_VARIETY(request):
    if request.method == "POST":
        variety_id = request.POST.get('variety_id')
        variety_image = request.FILES.get('variety_image')
        name = request.POST.get('name')
        description = request.POST.get('description')
        maturity_duration = request.POST.get('maturity_duration')
        yield_per_acre = request.POST.get('yield_per_acre')

        variety = Variety.objects.get(id = variety_id)
        variety.name = name
        variety.description = description
        variety.yield_per_acre = yield_per_acre
        variety.maturity_duration = maturity_duration
        
        if variety_image!=None and variety_image!="":
            variety.variety_image = variety_image
        variety.save()

        messages.success(request, "Record Successfully Updated !")

        return redirect("view_variety")

    return render(request,'admin/edit_variety.html')


# def DELETE_VARIETY(request,id):
#     variety = Variety.objects.get(id = id)
#     variety.delete()
#     messages.success(request, "Record Is Successfully Deleted!")
#     return redirect("view_variety")

from django.contrib import messages
from django.shortcuts import redirect

def DELETE_VARIETY(request, id):
    variety = Variety.objects.get(id=id)
    variety.delete()
    messages.success(request, "Record Is Successfully Deleted!")
    return redirect("view_variety")


# crop

def ADD_CROP(request):
    season = Season.objects.all()
    variety = Variety.objects.all()

    if request.method =="POST":
        name = request.POST.get('name')
        plant_type = request.POST.get('plant_type')
        soil_type = request.POST.get('soil_type')
        cultivation_type = request.POST.get('cultivation_type')
        name = request.POST.get('name')
        area = request.POST.get('area')
        description = request.POST.get('description')
        maturity_date = request.POST.get('maturity_date')
        sowing_date = request.POST.get('sowing_date')
        crop_image = request.FILES.get('crop_image')
        variety_id = request.POST.get('variety_id')
        season_id = request.POST.get('season_id')
        
        # print(variety_image,first_name,address,country_id, state_id,city_id,email)

        variety_id =Variety.objects.get(id = variety_id)
        season_id = Season.objects.get(id = season_id)
        
        crop = Crop(
            name = name,
            plant_type = plant_type,
            soil_type = soil_type,
            cultivation_type = cultivation_type,
            area = area,
            description = description,
            crop_image = crop_image,
            sowing_date = sowing_date,
            maturity_date = maturity_date,
            variety_id = variety_id,
            season_id = season_id,
        )
        crop.save()
        messages.success(request, crop.name + " Is Successfully Added!")
        return redirect('view_crop')

    context = {
        'variety': variety,
        'season' : season,
    } 

    return render(request, "admin/add_crop.html",context)    # return None

def VIEW_CROP(request):
    crop = Crop.objects.all()
    # print(grower)

    context = {
        'crop' : crop,
    }
    return render(request,'admin/view_crop.html',context)

def EDIT_CROP(request, id):
    crop = Crop.objects.filter(id = id)
    varieties = Variety.objects.all()
    seasons = Season.objects.all()
   
    context = {
        'crop' : crop,
        'varieties': varieties,
        'seasons' : seasons,
    }
    return render(request,'admin/edit_crop.html',context)

def UPDATE_CROP(request):
    if request.method == "POST":
        crop_id = request.POST.get('crop_id')
        name = request.POST.get('name')
        plant_type = request.POST.get('plant_type')
        soil_type = request.POST.get('soil_type')
        cultivation_type = request.POST.get('cultivation_type')
        name = request.POST.get('name')
        area = request.POST.get('area')
        description = request.POST.get('description')
        sowing_date = request.POST.get('sowing_date')
        maturity_date = request.POST.get('maturity_date')
        crop_image = request.FILES.get('crop_image')
        variety_id = request.POST.get('variety_id')
        season_id = request.POST.get('season_id')

        crop = Crop.objects.get(id = crop_id)
        crop.name = name
        crop.plant_type = plant_type
        crop.soil_type = soil_type
        crop.cultivation_type = cultivation_type
        crop.area = area
        crop.description = description
        crop.maturity_date = maturity_date
        crop.sowing_date = sowing_date
        # crop.crop_image = crop_image,
        
        if crop_image!=None and crop_image!="":
            crop.crop_image =crop_image
        # crop.save()

        # crop = Crop.objects.get(id = crop_id)
        
        variety = Variety.objects.get(id = variety_id)
        crop.variety_id = variety
        season = Season.objects.get(id = season_id)
        crop.season_id = season
       
        crop.save()
        messages.success(request, "Record Successfully Updated !")

        return redirect("view_crop")

    return render(request,'admin/edit_crop.html')

# def DELETE_CROP(request,id):
#     crop = Crop.objects.get(id = id)
#     crop.delete()
#     messages.success(request, "Record Is Successfully Deleted!")
#     return redirect("view_crop")

from django.contrib import messages
from django.shortcuts import redirect

def DELETE_CROP(request, id):
    crop = Crop.objects.get(id=id)
    crop.delete()
    messages.success(request, "Record Is Successfully Deleted!")
    return redirect("view_crop")

# agency
# agency

def ADD_AGENCY(request):
    country = Country.objects.all()
    state = State.objects.all()
    city = City.objects.all()

    if request.method =="POST":
        name = request.POST.get('name')
        address = request.POST.get('address')
        pin = request.POST.get('pin')
        establishment = request.POST.get('establishment')
        gst = request.POST.get('gst')
        contact_person = request.POST.get('contact_person')
        tan = request.POST.get('tan')
        website = request.POST.get('website')
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        country_id = request.POST.get('country_id')
        state_id= request.POST.get('state_id')
        city_id = request.POST.get('city_id')
        
        # print(variety_image,first_name,address,country_id, state_id,city_id,email)

        country_id =Country.objects.get(id = country_id)
        state_id = State.objects.get(id = state_id)
        city_id = City.objects.get(id=city_id)
        
        agency = Agency(
            name = name,
            address = address,
            pin=pin,
            establishment = establishment,
            gst = gst,
            contact_person =contact_person,
            tan = tan,
            website = website,
            mobile_number = mobile_number,
            email = email,
            country_id=country_id,
            state_id=state_id,
            city_id=city_id
        )
        agency.save()
        messages.success(request, agency.name + " Is Successfully Added!")
        return redirect('add_agency')

    context = {
        'country': country,
        'state' : state,
        'city': city
    } 

    return render(request, "admin/add_agency.html",context)    # return None

def VIEW_AGENCY(request):
    agency = Agency.objects.all()
    # print(grower)

    context = {
        'agency' : agency,
    }
    return render(request,'admin/view_agency.html',context)

def EDIT_AGENCY(request, id):
    agency = Agency.objects.filter(id = id)
    countries = Country.objects.all()
    states = State.objects.all()
    cities = City.objects.all()

    context = {
        'agency' : agency,
        'countries': countries,
        'states': states,
        'cities': cities
    }
    return render(request,'admin/edit_agency.html',context)

def UPDATE_AGENCY(request):
    countries = Country.objects.all()
    states = State.objects.all()
    cities = City.objects.all()

    if request.method == "POST":
        agency_id = request.POST.get('agency_id')
        name = request.POST.get('name')
        address = request.POST.get('address')
        pin = request.POST.get('pin')
        establishment = request.POST.get('establishment')
        gst = request.POST.get('gst')
        contact_person = request.POST.get('contact_person')
        tan = request.POST.get('tan')
        website = request.POST.get('website')
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        country_id = request.POST.get('country_id')
        state_id = request.POST.get('state_id')
        city_id = request.POST.get('city_id')

        print(country_id)

        agency = Agency.objects.get(id = agency_id)
        agency.name = name
        agency.address = address
        agency.pin = pin
        agency.establishment = establishment
        agency.gst = gst
        agency.contact_person = contact_person
        agency.tan = tan
        agency.website = website
        agency.mobile_number = mobile_number
        agency.email = email

        country = Country.objects.get(id = country_id)
        agency.country_id = country
        state = State.objects.get(id = state_id)
        agency.state_id = state
        city = City.objects.get(id=city_id)
        agency.city_id = city

        print(agency.country_id.id)
       
        agency.save()
        messages.success(request, "Record Successfully Updated !")

        return redirect("view_agency")
    
    else:
        # Retrieve the agency object for editing
        agency_id = request.GET.get('id')
        agency = Agency.objects.get(id=agency_id)

    context = {
        'agency': agency,
        'countries': countries,
        'states': states,
        'cities': cities
    }

    return render(request,'admin/edit_agency.html',context)

# def DELETE_AGENCY(request,id):
#     agency = Agency.objects.get(id = id)
#     agency.delete()
#     messages.success(request, "Record Is Successfully Deleted!")
#     return redirect("view_agency")

from django.contrib import messages
from django.shortcuts import redirect

def DELETE_AGENCY(request, id):
    agency = Agency.objects.get(id=id)
    agency.delete()
    messages.success(request, "Record Is Successfully Deleted!")
    return redirect("view_agency")


# branch

def ADD_BRANCH(request):
    country = Country.objects.all()
    state = State.objects.all()
    city = City.objects.all()
    agency = Agency.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        address = request.POST.get('address')
        pin = request.POST.get('pin')
        email = request.POST.get('email')
        country_id = request.POST.get('country_id')
        state_id = request.POST.get('state_id')
        city_id = request.POST.get('city_id')
        agency_id = request.POST.get('agency_id')

        # print(variety_image,first_name,address,country_id, state_id,city_id,email)

        country_id = Country.objects.get(id=country_id)
        state_id = State.objects.get(id=state_id)
        city_id = City.objects.get(id=city_id)
        agency_id = Agency.objects.get(id=agency_id)

        branch = Branch(
            name=name,
            address=address,
            pin=pin,
            email=email,
            country_id=country_id,
            state_id=state_id,
            city_id=city_id,
            agency_id = agency_id
        )
        branch.save()
        messages.success(request, branch.name + " Is Successfully Added!")
        return redirect('add_branch')

    context = {
        'country': country,
        'state': state,
        'city': city,
        'agency':agency
    }

    return render(request, "admin/add_branch.html", context)  # return None


def VIEW_BRANCH(request):
    branch = Branch.objects.all()
    # print(grower)

    context = {
        'branch': branch,
    }
    return render(request, 'admin/view_branch.html', context)


def EDIT_BRANCH(request, id):
    branch = Branch.objects.filter(id=id)
    countries = Country.objects.all()
    states = State.objects.all()
    cities = City.objects.all()
    agencies = Agency.objects.all()

    context = {
        'branch':branch,
        'agencies': agencies,
        'countries': countries,
        'states': states,
        'cities': cities
    }
    return render(request, 'admin/edit_branch.html', context)


def UPDATE_BRANCH(request):
    if request.method == "POST":
        branch_id = request.POST.get('branch_id')
        name = request.POST.get('name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        country_id = request.POST.get('country_id')
        state_id = request.POST.get('state_id')
        city_id = request.POST.get('city_id')
        agency_id = request.POST.get('agency_id')

        branch = Branch.objects.get(id=branch_id)
        branch.name = name
        branch.address = address
        branch.email = email

        # crop.save()

        # crop = Crop.objects.get(id = crop_id)

        country = Country.objects.get(id=country_id)
        branch.country_id = country
        state = State.objects.get(id=state_id)
        branch.state_id = state
        city = City.objects.get(id=city_id)
        branch.city_id = city
        agency = Agency.objects.get(id=agency_id)
        branch.agency_id = agency

        branch.save()
        messages.success(request, "Record Successfully Updated !")

        return redirect("view_branch")

    return render(request, 'admin/edit_branch.html')


# def DELETE_BRANCH(request, id):
#     branch = Branch.objects.get(id=id)
#     branch.delete()
#     messages.success(request, "Record Is Successfully Deleted!")
#     return redirect("view_branch")

from django.contrib import messages
from django.shortcuts import redirect

def DELETE_BRANCH(request, id):
    branch = Branch.objects.get(id=id)
    branch.delete()
    messages.success(request, "Record Is Successfully Deleted!")
    return redirect("view_branch")


@login_required(login_url='/')
# from django.shortcuts import render, redirect
# from .models import Field_worker, Grower, CustomUser

def ADD_FIELDWORKERS(request):
    if request.method == 'POST':
        profile_pic = request.FILES['profile_pic']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        gender = request.POST['gender']
        dob = request.POST['dob']
        phone_number = request.POST['phone_number']
        agency_id = request.POST['agency_id']
        branch_id = request.POST['branch_id']
        grower = request.POST['grower']
        
        # Save the custom user
        user = CustomUser.objects.create(
            profile_pic = profile_pic,
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            # password=password,
            user_type=2,  # Set user_type to 'GROWER'
        )
        user.set_password(password)
        user.save()
        
        # Save the grower
        # grower = Grower.objects.get(id=grower_id)
        # grower.admin = user
        # grower.save()
        
        # Get the agency instance
        agency = Agency.objects.get(id=agency_id)
        branch = Branch.objects.get(id=branch_id)
        
        # Save the field worker
        fieldworker = Field_worker.objects.create(
            admin=user,
            gender=gender,
            dob=dob,
            phone_number=phone_number,
            agency_id=agency,
            branch_id=branch,
            grower=grower
        )
        
        # Save the profile picture
        # fieldworker.admin.profile_pic = profile_pic
        fieldworker.save()
        
        return redirect('view_fieldworkers')  # Replace 'fieldworkers_list' with your actual URL name for the fieldworker list page
    
    context = {
        # 'grower': Grower.objects.all(),
        'agency': Agency.objects.all(),
        'branch': Branch.objects.all()
    }
    
    return render(request, "admin/add_fieldworkers.html", context)

# def ADD_FIELDWORKERS(request):
#     branch = Branch.objects.all()
#     agency = Agency.objects.all()
#     grower = Grower.objects.all()

#     if request.method =="POST":
#         profile_pic = request.FILES.get('profile_pic')
#         # examination_image = request.FILES.get('examination_image')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         # global email
#         email = request.POST.get('email')
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         gender = request.POST.get('gender')
#         dob = request.POST.get('dob')
#         phone_number = request.POST.get('phone_number')
#         branch_id = request.POST.get('branch_id')
#         agency_id = request.POST.get('agency_id')
#         grower_id = request.POST.get('grower_id')

#         if CustomUser.objects.filter(email = email).exists() :
#             messages.warning(request,"Email Is Already Taken")
#             return redirect('add_fieldworkers') 
#         if CustomUser.objects.filter(username = username).exists():
#             messages.warning(request,"Username Is Already Taken")
#             return redirect('add_fieldworkers')
#         else:
#             user = CustomUser(
#                 first_name = first_name,
#                 last_name = last_name,
#                 username = username,
#                 email = email,
#                 profile_pic = profile_pic,
#                 user_type = 2,
#             )
#             user.set_password(password)
#             user.save()

#             branch_id = Branch.objects.get(id=branch_id)
#             agency_id = Agency.objects.get(id=agency_id)
#             # grower_id = Grower.objects.get(id=grower_id)
#             grower_id = Grower.objects.get(admin=grower_id)
#             # agency_id = Agency.objects.get(id=agency_id)
#             print("Grower ID:", grower_id)

#             fieldworker = Field_worker(
#                 admin = user,
#                 gender=gender,
#                 dob = dob,
#                 phone_number = phone_number,
#                 branch_id =branch_id,
#                 agency_id =agency_id,
#                 grower_id=grower_id
#                 # grower_id = grower_id,
#             )

#             fieldworker.save()
#             messages.success(request, fieldworker.admin.first_name + " Is Successfully Added!")
#             return redirect('view_fieldworkers')

#     context = {
#         'branch': branch,
#         'agency':agency,
#         'grower':grower,
#     }

#     return render(request, "admin/add_fieldworkers.html", context)

def VIEW_FIELDWORKERS(request):
    fieldworker = Field_worker.objects.all()
    # print(grower)

    context = {
        'fieldworker': fieldworker,
    }
    return render(request, 'admin/view_fieldworkers.html', context)

def EDIT_FIELDWORKERS(request,id):
    fieldworker = Field_worker.objects.filter(id=id)
    branches = Branch.objects.all()
    agencies = Agency.objects.all()
    # grower = Grower.objects.all()

    context = {
        'fieldworker': fieldworker,
        'agencies': agencies,
        'branches': branches,
        # 'grower':grower,

    }
    return render(request, 'admin/edit_fieldworkers.html', context)


def UPDATE_FIELDWORKERS(request):
    if request.method == 'POST':
        fieldworker_id = request.POST.get('fieldworker_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        phone_number = request.POST.get('phone_number')
        agency_id = request.POST.get('agency_id')
        branch_id = request.POST.get('branch_id')
        grower= request.POST.get('grower')

        user = CustomUser.objects.get(id = fieldworker_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        # Update password only if a new password is provided
        if password!=None and password!="":
            user.set_password(password)
        if profile_pic!=None and profile_pic!="":
            user.profile_pic = profile_pic
        user.save()

        fieldworker = Field_worker.objects.get(admin = fieldworker_id)

        fieldworker.gender = gender
        fieldworker.dob = dob
        fieldworker.phone_number = phone_number
        fieldworker.grower = grower

        # Retrieve the Agency and Branch instances
        agency = Agency.objects.get(id=agency_id)
        branch = Branch.objects.get(id=branch_id)
        # grower = Grower.objects.get(id=grower_id)

        fieldworker.agency_id = agency
        fieldworker.branch_id = branch
        

        # fieldworker.admin.save()
        fieldworker.save()

        # Redirect to a success page or any other desired URL
        return redirect('view_fieldworkers')

    # Render the form template if it's a GET request
    return render(request, 'admin/edit_grower.html')


from django.core.exceptions import ObjectDoesNotExist
def DELETE_FIELDWORKERS(request, admin):
    fieldworker = CustomUser.objects.get(id=admin)
    fieldworker.delete()
    messages.success(request, "Record Is Successfully Deleted!")
    return redirect("view_fieldworkers")
# def DELETE_FIELDWORKERS(request, admin):
#     try:
#         fieldworker = CustomUser.objects.get(id=admin)
#         fieldworker.delete()
#         messages.success(request, "Record Is Successfully Deleted!")
#     except ObjectDoesNotExist:
#         messages.error(request, "Fieldworker does not exist.")
#     return redirect("view_fieldworkers")
    

# def UPDATE_FIELDWORKERS(request):
#     if request.method == "POST":
#         # selected_value = request.POST.get('my_dropdown')
#         fieldworker_id = request.POST.get('fieldworker_id')
#         profile_pic = request.FILES.get('profile_pic')
#         # examination_image= request.FILES.get('examination_image')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         # global email
#         email = request.POST.get('email')
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         gender = request.POST.get('gender')
#         dob = request.POST.get('dob')
#         phone_number = request.POST.get('phone_number')
#         agency_id = request.POST.get('agency_id')
#         branch_id = request.POST.get('branch_id')
#         # print(profile_pic, grower_id)

#         user = CustomUser.objects.get(id = fieldworker_id)
#         user.first_name = first_name
#         user.last_name = last_name
#         user.email = email
#         user.username = username
        
#         if password!=None and password!="":
#             user.set_password(password)
#         if profile_pic!=None and profile_pic!="":
#             user.profile_pic = profile_pic
#         user.save()

#         fieldworker = Field_worker.objects.get(admin = fieldworker_id)
#         fieldworker.gender = gender
#         fieldworker.dob =dob
#         fieldworker.phone_number = phone_number
        
#         agency = Agency.objects.get(id=agency_id)
#         fieldworker.agency_id = agency
#         branch = Branch.objects.get(id=branch_id)
#         fieldworker.branch_id = branch

#         fieldworker.save()
#         messages.success(request, "Record Successfully Updated !")

#         return redirect("view_grower")

#     return render(request,'admin/edit_grower.html')

from django.views.decorators.csrf import csrf_exempt

# 2. Exempt the view from CSRF checks
@csrf_exempt
def state_api(request):
    # if request.method == "GET":
    #     result = []

    #     st = Season.objects.all()
    #     for s in st:
    #         data = {
    #             "name":s.name,
    #             "season_from_date":s.from_date,
    #             "season_to_date":s.to_date,
    #             # "description":s.description
    #         }
    #         result.append(data)
        
    #     return HttpResponse(json.dumps(result))
    
    # if request.method == "POST":
    #     body_unicode = request.body.decode('utf-8')

    #     print(request.body)
    #     print(body_unicode)
    #     data = json.loads(body_unicode)

    #     name = data['name']
    #     season_from_date = data['season_from_date']
    #     season_to_date = data['season_to_date']

    #     for s in Season.objects.all():
    #         if s.name == name:
    #             return HttpResponse("Season already exists",status=404)

    #     st = Season(name=name,from_date=season_from_date,to_date=season_to_date)
    #     st.save()
    #     return HttpResponse({"Season added successfully"})

    if request.method == "DELETE":
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)

        name = data['name']
        d=[]
        st = Season.objects.all()
        for s in st:
            d.append(s.name)
        
        if name not in d:
            return HttpResponse("State not exists",status=404)
        
        st = Season.objects.filter(name=name).delete()
        return HttpResponse("State deleted successfully")
    
