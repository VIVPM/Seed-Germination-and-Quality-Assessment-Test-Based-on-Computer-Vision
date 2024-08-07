"""seed_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.auth import views as auth_views 
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph


from . import views,grower_views, admin_views,agency_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base', views.BASE, name ="base"),
    path('about', views.ABOUT, name ="about"),
    # login
    path('', views.LOGIN, name ="login"),#login path
    path('doLogin', views.doLogin, name ="doLogin"),#login path
    path('doLogout', views.doLogout, name ="logout"),#login path
    path('register/', views.register, name='register'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('profilegrower', views.profilegrower, name='profilegrower'),
    path('profilefieldworker', views.profilefieldworker, name='profilefieldworker'),
    # path('grower/', views.grower, name='grower'),

    # profile update
    path('profile',views.PROFILE, name = "profile"),
    path('profile/update',views.PROFILE_UPDATE, name = "profile_update"),

    # admin url
    path("Admin/home",admin_views.HOME, name = "admin_home"),
    path('Admin/Contact', admin_views.contact, name='admin_contact'),
    path('Admin/About', admin_views.about, name='admin_about'),
    path("Admin/Grower/Add",admin_views.ADD_GROWER, name="add_grower"),
    path("Admin/Grower/View",admin_views.VIEW_GROWER, name="view_grower"),
    path("Admin/Grower/Edit/<str:id>",admin_views.EDIT_GROWER, name="edit_grower"),
    path("Admin/Grower/Update",admin_views.UPDATE_GROWER, name="update_grower"),
    path("Admin/Grower/Delete/<str:admin>",admin_views.DELETE_GROWER, name="delete_grower"),
   
#    season
    path("Admin/Season/Add",admin_views.ADD_SEASON, name="add_season"),
    # path("Admin/Season/Add",admin_views.state_api, name="state_api"),
    path("Admin/Season/View",admin_views.VIEW_SEASON, name="view_season"),
    path("Admin/Season/Edit/<str:id>",admin_views.EDIT_SEASON, name="edit_season"),
    path("Admin/Season/Update",admin_views.UPDATE_SEASON, name="update_season"),
    path("Admin/Season/Delete/<str:id>",admin_views.DELETE_SEASON, name="delete_season"),
    # path("Admin/Season/Delete/<str:id>",admin_views.state_api, name="state_api"),
#   variety
    path("Admin/Variety/Add",admin_views.ADD_VARIETY, name="add_variety"),
    path("Admin/Variety/View",admin_views.VIEW_VARIETY, name="view_variety"),
    path("Admin/Variety/Edit/<str:id>",admin_views.EDIT_VARIETY, name="edit_variety"),
    path("Admin/Variety/Update",admin_views.UPDATE_VARIETY, name="update_variety"),
    path("Admin/Variety/Delete/<str:id>",admin_views.DELETE_VARIETY, name="delete_variety"),
   

#    crop 
    path("Admin/Crop/Add",admin_views.ADD_CROP, name="add_crop"),
    path("Admin/Crop/View",admin_views.VIEW_CROP, name="view_crop"),
    path("Admin/Crop/Edit/<str:id>",admin_views.EDIT_CROP, name="edit_crop"),
    path("Admin/Crop/Update",admin_views.UPDATE_CROP, name="update_crop"),
    path("Admin/Crop/Delete/<str:id>",admin_views.DELETE_CROP, name="delete_crop"),
#    agency
    path("Admin/Agency/Add",admin_views.ADD_AGENCY, name="add_agency"),
    path("Admin/Agency/View",admin_views.VIEW_AGENCY, name="view_agency"),
    path("Admin/Agency/Edit/<str:id>",admin_views.EDIT_AGENCY, name="edit_agency"),
    path("Admin/Agency/Update",admin_views.UPDATE_AGENCY, name="update_agency"),
    path("Admin/Agency/Delete/<str:id>",admin_views.DELETE_AGENCY, name="delete_agency"),
#    branch
    path("Admin/Branch/Add",admin_views.ADD_BRANCH, name="add_branch"),
    path("Admin/Branch/View",admin_views.VIEW_BRANCH, name="view_branch"),
    path("Admin/Branch/Edit/<str:id>",admin_views.EDIT_BRANCH, name="edit_branch"),
    path("Admin/Branch/Update",admin_views.UPDATE_BRANCH, name="update_branch"),
    path("Admin/Branch/Delete/<str:id>",admin_views.DELETE_BRANCH, name="delete_branch"),
#    fieldworker
    path("Admin/Fieldworker/Add",admin_views.ADD_FIELDWORKERS, name="add_fieldworkers"),
    path("Admin/Fieldworker/View",admin_views.VIEW_FIELDWORKERS, name="view_fieldworkers"),
    path("Admin/Fieldworker/Edit/<str:id>",admin_views.EDIT_FIELDWORKERS, name="edit_fieldworkers"),
    path("Admin/Fieldworker/Update",admin_views.UPDATE_FIELDWORKERS, name="update_fieldworkers"),
    path("Admin/Fieldworker/Delete/<str:admin>",admin_views.DELETE_FIELDWORKERS, name="delete_fieldworkers"),

    # grower
    path("Grower/Home", grower_views.Home,name='grower_home'),
    path("Grower/About", grower_views.about,name='grower_about'),
    path("Grower/Contact", grower_views.contact,name='grower_contact'),
    path('Grower/AddDetails',grower_views.add_details, name = "add_details"),
    path("Grower/Update",grower_views.update_details, name="update_details"),
    path('Grower/Testing',grower_views.testing_page, name = "testing_page"),
    path('Grower/predictImage',grower_views.predictImage, name = "predict_image"),
    path('Grower/exportPdf/<str:classification_result>',grower_views.export_pdf,name = "export_pdf"),

    # field worker
    path("Agency/Home", agency_views.Home,name='agency_home'),
    # path("Agency/Home", agency_views.Home,name='agency_home'),
    path("Agency/About", agency_views.about,name='agency_about'),
    path("Agency/Contact", agency_views.contact,name='agency_contact'),
    path('Agency/AddDetails',agency_views.add_details, name = "agency_add_details"),
    path("Agency/Update",agency_views.update_details, name="agency_update_details"),
    path('Agency/Testing',agency_views.testing_page, name = "agency_testing_page"),
    path('Agency/predictImage',agency_views.predictImage, name = "agency_predict_image"),
    path('Agency/exportPdf/<str:classification_result>/',agency_views.export_pdf,name = "agency_export_pdf"),

    path('forget-password' , views.ForgetPassword , name="forget_password"),
    path('change-password/<token>/' , views.ChangePassword , name="change_password"),
    

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


