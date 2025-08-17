from django.contrib import admin
from folhadeponto import models

for model in [
    models.Funcao,
    models.Area,
    models.Setor,
    models.Usuario
]:
    admin.site.register(model)

class CarreiraAdmin(admin.ModelAdmin):
  list_display = ("nome", "data_cadastro",)
admin.site.register(models.Carreira, CarreiraAdmin)

class CargoAdmin(admin.ModelAdmin):
    list_display = ("nome", "nivel", "data_cadastro")
admin.site.register(models.Cargo, CargoAdmin)

class ServidorAdmin(admin.ModelAdmin):
    list_display = ("nome", "matricula", "data_exercicio", "data_cadastro")
admin.site.register(models.Servidor, ServidorAdmin)

class DatasAdmin(admin.ModelAdmin):
    list_display  = ("nome", "data", "tipo")
admin.site.register(models.Data, DatasAdmin)

class FolhasAdmin(admin.ModelAdmin):
    list_display  = ("mes_ano", "setor_mes_ano", "data_cadastro")
admin.site.register(models.Folha, FolhasAdmin)

class CampiAdmin(admin.ModelAdmin):
    list_display  = ("nome", "sigla", "data_cadastro")
admin.site.register(models.Campus, CampiAdmin)

