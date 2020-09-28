from django.contrib import admin
from .models import RespondentProfile, YaridMemberRole, Messages, StaffMemberProfile, \
    YaridAccount, \
    CarouselDisplay, SurveyTopics, Kudos, QuestionPosts


# from .models import Subjects, MemberProfile, NewsPosts, Marks, Messages


#

# Register your models here.
@admin.register(RespondentProfile)
class RespondentProfile(admin.ModelAdmin):
    list_display = (
        'RespondentName',
        'RespondentRole')
    list_filter = ('RespondentName',)
    search_fields = ('RespondentName', 'RespondentRole')


@admin.register(StaffMemberProfile)
class StaffMemberProfile(admin.ModelAdmin):
    list_display = (
        'StaffMemberId',
        'StaffMemberRole', 'StaffMemberprofiling_date')
    list_filter = ('StaffMemberId', 'StaffMemberprofiling_date')
    search_fields = ('StaffMemberId', 'StaffMembercourse')
    ordering = ('StaffMemberprofiling_date', 'StaffMemberId')


@admin.register(YaridMemberRole)
class YaridMemberRole(admin.ModelAdmin):
    list_display = ('role_name', 'role_name_added_date')


@admin.register(SurveyTopics)
class SurveyTopics(admin.ModelAdmin):
    list_display = ('survey_name', 'added_date')


@admin.register(Kudos)
class Marks(admin.ModelAdmin):
    list_display = ('respondent_marked', 'survey_marked', 'survey_marks', 'recorded_by', 'posting_date')
    list_filter = ('respondent_marked', 'survey_marked', 'recorded_by')
    search_fields = ('respondent_marked', 'recorded_by')
    ordering = ('recorded_by', 'respondent_marked')


@admin.register(QuestionPosts)
class QuestionPosts(admin.ModelAdmin):
    list_display = ('poster_name', 'post_title', 'post_body', 'posting_date')
    list_filter = ('poster_name', 'post_title', 'posting_date', 'post_title')
    search_fields = ('poster_name', 'post_title')
    ordering = ('posting_date', 'poster_name')


@admin.register(Messages)
class Messages(admin.ModelAdmin):
    list_display = ('sendername', 'recievername', 'messagetitle', 'messagebody', 'sendingDate')
    list_filter = ('sendername', 'recievername', 'messagetitle')
    search_fields = ('sendername', 'recievername')
    ordering = ('sendername', 'sendingDate')


@admin.register(YaridAccount)
class YaridAccount(admin.ModelAdmin):
    list_display = ('name', 'lastname', 'Uemail', 'password','residence',
                    'reg_date','country_of_origin')
    list_filter = ('name', 'Uemail', 'reg_date')
    search_fields = ('name', 'Uemail')
    ordering = ('reg_date', 'name')


@admin.register(CarouselDisplay)
class CarouselDisplay(admin.ModelAdmin):
    list_display = ('title', 'body', 'image', 'creationDate')
    list_filter = ('title', 'body', 'creationDate')
    search_fields = ('title', 'image')
    ordering = ('creationDate','image')

