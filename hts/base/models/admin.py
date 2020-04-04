from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from misago.threads.models.thread import Thread


@modeladmin_register
class ThreadModelAdmin(ModelAdmin):
    model = Thread
    menu_label = "Community Discussions"
    menu_icon = "bubble"
    list_display = ('title', 'category', 'started_on', 'starter_name')
    list_filter = ('category',)
    search_fields = ('title',)