from django.contrib import admin

from apps.exercise.models import Exercise, Method, MuscularGroup, Objective


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'muscular_group', 'objective', 'video_display']
    search_fields = ['name', 'muscular_group__name', 'objective__name']
    list_filter = ['muscular_group', 'objective']
    ordering = ['name', 'muscular_group__name', 'objective__name']

    def video_display(self, obj):
        if obj.has_video:
            return '✓'
        else:
            return '✗'
        
    video_display.short_description = '¿Tiene vídeo?'
    
class MethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    ordering = ['name']
    
class MuscularGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']

class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']

admin.site.register(MuscularGroup, MuscularGroupAdmin)
admin.site.register(Objective, ObjectiveAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Method, MethodAdmin)