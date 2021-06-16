from django.contrib import admin
from .models import Sp, Build

class SpAdmin(admin.ModelAdmin):
    list_display = ('name', 'wiki', 'category', 'project_name')
    list_filter = ['category']
    search_fileds = ['name']

class BuildAdmin(admin.ModelAdmin):
    list_display = ('name', 'sp_name','wiki', 'release_note', 'release_date')
    search_fileds = ['name']
    def sp_name(self, obj):
        sp = Sp.objects.get(id=obj.sp_id_fk.id)
        return '{}'.format(sp.name)
    sp_name.short_description = 'SP'

admin.site.register(Sp, SpAdmin)
admin.site.register(Build, BuildAdmin)
