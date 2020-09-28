from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets, generics, status, parsers, response, decorators
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import *
from .models import RespondentProfile, StaffMemberProfile, CarouselDisplay, Kudos


class UserCreate(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    queryset = YaridAccount.objects.order_by('-id')
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()

    def post(self, request, ):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key, "username": user.username})
            # return Response({"token": "logged in"})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class Respondents(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = RespondentProfile.objects.order_by('-id')
    serializer_class = RespondentProfileSerializers

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied(
                request.user.username + " You can not delete this studentProfile. Only Marks_Recorders are deleters")
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied(
                request.user.username + " You can not delete this studentProfile. Only Marks_Recorders are deleters")
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied(
                request.user.username + " You can not update this studentProfile. Only Marks_Recorders are updaters")
        return super().update(request, *args, **kwargs)


class SurveyTopics(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = SurveyTopics.objects.order_by('-id')
    serializer_class = SurveyTopicsSerializers

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied(
                request.user.username + " You can not create this course, you dont have the rights to")
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        course = SurveyTopics.objects.get(pk=self.kwargs["pk"])
        if not request.user == course.poster_name:
            raise PermissionDenied(
                request.user.username + " You can not delete this course. Only Marks_Recorders are deleters")
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        course = SurveyTopics.objects.get(pk=self.kwargs["pk"])
        if not request.user == course.poster_name:
            raise PermissionDenied(
                request.user.username + " You can not update this course. Only Marks_Recorders are updaters")
        return super().update(request, *args, **kwargs)


class Kudos(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Kudos.objects.order_by('-id')
    serializer_class = KudosSerializers

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied(
                request.user.username + " You can not create this course, you dont have the rights to")
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        marks = Kudos.objects.get(pk=self.kwargs["pk"])
        if not request.user == marks.poster_name:
            raise PermissionDenied(
                request.user.username + " You can not delete the Marks. Only Marks_Recorders are deleters")
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        marks = Kudos.objects.get(pk=self.kwargs["pk"])
        if not request.user == marks.poster_name:
            raise PermissionDenied(
                request.user.username + " You can not update the Marks. Only Marks_Recorders are updaters")
        return super().update(request, *args, **kwargs)


class QuestionPostsView(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, IsAdminUser)  # used for allowing admins only
    queryset = QuestionPosts.objects.order_by('-id')
    serializer_class = NewsPostsSerializers

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied(
                request.user.username + " You were not authenticated ")
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        newspost = QuestionPosts.objects.get(pk=self.kwargs["pk"])
        if not request.user == newspost.poster_name:
            raise PermissionDenied(
                request.user.username + " You can not delete this newspost. Only creaters are deleters")
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        newspost = QuestionPosts.objects.get(pk=self.kwargs["pk"])
        if not request.user == newspost.poster_name:
            raise PermissionDenied(
                request.user.username + " You can not update this newspost. Only creaters are updaters")
        return super().update(request, *args, **kwargs)


class CarouselDisplay(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = CarouselDisplay.objects.order_by('-id')
    serializer_class = CarouselDisplaySerializers


# this is to help in posting base64 images
# class ProfileViewSet(viewsets.ModelViewSet):
#     serializer_class = ProfileSerializer
#     queryset = Profile.objects.all()
#
#     @decorators.action(
#         detail=True,
#         methods=['PUT'],
#         serializer_class=ProfilePicSerializer,
#         parser_classes=[parsers.MultiPartParser],
#     )
#     def pic(self, request, pk):
#         obj = self.get_object()
#         serializer = self.serializer_class(obj, data=request.data,
#                                            partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return response.Response(serializer.data)
#         return response.Response(serializer.errors,
#                                  status.HTTP_400_BAD_REQUEST)



@api_view(['GET', ])
def getallstudentprofiles(self):
    students = RespondentProfile.objects.all()
    serializer = RespondentProfileSerializers(students, many=True)
    return Response({"all students": serializer.data})


@api_view(['GET', 'POST'])
def obtain_auth_token(self):
    for user in User.objects.all():
        Token.objects.get_or_create(user=user)
    return Response({"all students": "created tokens for the already existant users"})

# class SysUserCreation(generics.CreateAPIView):
#     authentication_classes = ()
#     permission_classes = ()
#     serializer_class = CreatingSysUsers
