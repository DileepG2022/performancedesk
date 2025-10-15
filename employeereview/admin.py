from django.contrib import admin

from .models import Metric

# Register your models here.
class MetricAdmin(admin.ModelAdmin):
    list_display = ('metric_name', 'group', 'metric_datatype', 'order', 'isactive')
    list_filter = ('group', 'metric_datatype', 'isactive')
    search_fields = ('metric_name',)
    exclude = ['created_user']
    # To save the logged in user id to the table when a record is added.
    # https://stackoverflow.com/questions/6760602/how-can-i-get-current-logged-user-id-in-django-admin-panel
    def save_model(self, request, obj, form, change):
        obj.created_user = request.user
        #print(eval(self._class.name_))
        super().save_model(request, obj,form,change)

# class MilestoneActivityAdmin(admin.ModelAdmin):
#     list_display = ('activity', 'group', 'day', 'isactive')
#     list_filter = ('group', 'isactive')
#     search_fields = ('activity',)
#     exclude = ['created_user']
#     def save_model(self, request, obj, form, change):
#         obj.created_user = request.user
#         #print(eval(self._class.name_))
#         super().save_model(request, obj,form,change)

admin.site.register(Metric, MetricAdmin)
# admin.site.register(MilestoneActivity, MilestoneActivityAdmin)