from django.urls import path, include
from rest_framework import routers

from . import views
from .views import *

router = routers.DefaultRouter()
router.register('respondents', views.Respondents)
router.register('surveyTopics', views.SurveyTopics)
router.register('kudos', views.Kudos)
router.register('registration', views.UserCreate)
router.register('newsposts', views.QuestionPostsView)
router.register('carouseldisplay', views.CarouselDisplay)
# router.register('profiles', views.ProfileViewSet)

app_name = 'API'

urlpatterns = [

    path('', include(router.urls)),
    path('respondentsprofiles/', views.getallstudentprofiles, name='allrespondents'),
    path("login/", LoginView.as_view(), name="login"),
    path("obtain/", views.obtain_auth_token, name="obtain")
]