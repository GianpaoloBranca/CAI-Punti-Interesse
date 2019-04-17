from django.contrib import admin

from punti_interesse import models

class PuntoInteresseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome', )}

admin.site.register(models.PuntoInteresse, PuntoInteresseAdmin)
admin.site.register(models.ValidazionePunto)
admin.site.register(models.FotoAccessoria)
admin.site.register(models.TipoInteresse)
admin.site.register(models.InteresseSpecifico)
admin.site.register(models.QualitaInteresse)
admin.site.register(models.EstensioneInteresse)
admin.site.register(models.StatoConservazione)
admin.site.register(models.GruppoMontuoso)
admin.site.register(models.UserInfo)
