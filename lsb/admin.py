from django.contrib import admin

from lsb.models import Penyisipan, Ekstraksi, AktivitasPengguna

# Register your models here.

class SetModelPenyisipan(admin.ModelAdmin):
	class Meta:
		model = Penyisipan
		fields = '__all__'

class SetModelEkstraksi(admin.ModelAdmin):
	class Meta:
		model = Ekstraksi
		fields = '__all__'

admin.site.register(Penyisipan, SetModelPenyisipan)
admin.site.register(Ekstraksi, SetModelEkstraksi)
admin.site.register(AktivitasPengguna)