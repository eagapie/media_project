from django.contrib    import admin
from mediacloud.models import Story, Media, Companies, MediaCategory

class StoryAdmin(admin.ModelAdmin):
    list_display  = ('story_id', 'media', 'publish_date', 'story_text', 'companies')
#    list_filter = ('media', 'story_id')
    search_fields = [ 'story_text' ]
#    inlines = [Media]
admin.site.register(Story,StoryAdmin)


class MediaAdmin(admin.ModelAdmin):
    list_display  = ('media_id', 'name', 'category', 'url')
    search_fields = [ 'name', 'url' ]
    #list_filter   = ('category', )
admin.site.register(Media, MediaAdmin)


class MediaCategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
admin.site.register(MediaCategory, MediaCategoryAdmin)


class CompaniesAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Companies, CompaniesAdmin)

