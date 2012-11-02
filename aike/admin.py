from django.contrib import admin

from apps.zonas import models

class AikeAdminSite(admin.AdminSite):
    pass

class AlturaInlineAdmin(admin.TabularInline):
    model = models.Altura
    extra = 1

class CalleModelAdmin(admin.ModelAdmin):
    inlines = [ AlturaInlineAdmin ]

aike_site = AikeAdminSite("nombdre")
aike_site.register(models.Localidad)
aike_site.register(models.Calle, CalleModelAdmin)
