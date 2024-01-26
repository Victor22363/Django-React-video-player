from django.contrib import admin
from .models import *
# Register your models here.


class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'show', 'season', 'epNum', 'file')
    list_filter = ('id', 'title', 'show', 'season', 'epNum', 'tags' , 'file')
    filter_horizontal= ('tags',)
admin.site.register(Video, VideoAdmin)

class SeasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'show', 'seasonNum')
admin.site.register(Season, SeasonAdmin)

class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
admin.site.register(Tag, TagsAdmin)

class ShowAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
admin.site.register(Show, ShowAdmin)