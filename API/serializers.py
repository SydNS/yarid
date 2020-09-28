from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from rest_framework.response import Response

from .models import ( CarouselDisplay, Kudos, SurveyTopics,
                     RespondentProfile, YaridAccount, QuestionPosts)


# ...creating a user
class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = YaridAccount
        fields = ('name', 'lastname', 'Uemail', 'residence', 'country_of_origin', 'password1', 'password2')
        depth = 1

    def create(self, validated_data):
        Uemail = self.validated_data['Uemail']
        lastname = self.validated_data['lastname']
        name = self.validated_data['name']
        residence = self.validated_data['residence']
        country_of_origin = self.validated_data['country_of_origin']
        password1 = self.validated_data['password1']
        password2 = self.validated_data['password2']
        # photo = self.validated_data['photo']

        if password1 != password2:
            return Response({"Message": "Passwords Dont match Correct this"})

        yariduser = YaridAccount(lastname=lastname, name=name, password=password1,
                                 Uemail=Uemail,
                                 country_of_origin=country_of_origin,
                                 residence=residence)
        yariduser.save()
        uname = str(lastname) + ' ' + str(name)
        user = User(email=Uemail, username=uname)
        user.set_password(password2)
        user.save()
        Token.objects.create(user=user)

        return yariduser


class CreatingSysUsers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(email=validated_data['email'], username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class RespondentProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = RespondentProfile
        fields = ('RespondentName', 'RespondentRole', 'Respondentprofiling_date')
        depth = 1


class SurveyTopicsSerializers(serializers.ModelSerializer):
    class Meta:
        model = SurveyTopics
        fields = ('survey_name', 'added_date')
        depth = 1


class KudosSerializers(serializers.ModelSerializer):
    class Meta:
        model = Kudos
        fields = ('respondent_marked', 'survey_marked', 'survey_marks', 'recorded_by', 'posting_date')
        depth = 3


class NewsPostsSerializers(serializers.ModelSerializer):
    class Meta:
        model = QuestionPosts
        fields = ('poster_name', 'post_title', 'post_body', 'posting_date', 'post_image')
        depth = 0


class CarouselDisplaySerializers(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = CarouselDisplay
        fields = ['title', 'image', 'body', 'creationDate']
        depth = 1

# this is to help in posting base64 images
# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['name', 'bio', 'pic']
#         read_only_fields = ['pic']
#
#
# class ProfilePicSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['pic']
