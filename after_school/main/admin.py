from django.apps import apps
from django.contrib import admin

@admin.register(apps.get_model('main', 'choice'))
class ChoiceAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print(apps.get_model('main', 'Event').objects.filter(event_group__type='C'))
        if db_field.name == "event":
            kwargs["queryset"] = apps.get_model('main', 'Event').objects.filter(event_group__type='C')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


for model in apps.get_app_config('main').get_models():

    models_to_ignore = [  
        'main.choice'
   ]  
    if model._meta.label_lower in models_to_ignore  :
        continue

    admin.site.register(model)

