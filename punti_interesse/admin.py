from django.contrib import admin

from punti_interesse.models import *

class PuntoInteresseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nome', )}

admin.site.register(PuntoInteresse, PuntoInteresseAdmin)
admin.site.register(TipoInteresse)
admin.site.register(InteresseSpecifico)
admin.site.register(QualitaInteresse)
admin.site.register(EstensioneInteresse)
admin.site.register(ValidazionePunto)
admin.site.register(FotoAccessoria)
