from django.contrib import admin
# from django.utils.translation import gettext_lazy as _
from django.apps import apps

# Reemplaza con el nombre exacto de tu app como aparece en INSTALLED_APPS
app = apps.get_app_config('appAdmin')

for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass



# # Register your models here.
# class AgentAdmin(admin.ModelAdmin):
#     list_display = ('name', 'available')
#     list_display_links = ('name', 'available')
#     ordering = ('name',)

#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()
#     search_fields = ('name',)
#     list_per_page = 25

# class TagAdmin(admin.ModelAdmin):
#     list_display = ('name', 'color')
#     list_display_links = ('name', 'color')
#     ordering = ('name',)

#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()
#     search_fields = ('name',)


# admin.site.register(Agent, AgentAdmin)
# admin.site.register(Tag, TagAdmin)