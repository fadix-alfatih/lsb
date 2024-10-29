from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from lsb.functions import nama_gambar

# Create your models here.
class Penyisipan(models.Model):
	id = models.CharField(primary_key=True, max_length=10, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	nama = models.CharField(max_length=256, null=True)
	gambar = models.ImageField(upload_to='penyisipan/', blank=False, null=False)
	psnr = models.FloatField(null=True)
	mse = models.FloatField(null=True)
	waktu = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.id

	def namagambar(self):
		return nama_gambar(self.gambar.name)

	class Meta:
		ordering = ['-waktu']


class Ekstraksi(models.Model):
	id = models.CharField(primary_key=True, max_length=10, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	nama = models.CharField(max_length=256, null=True)
	gambar = models.ImageField(upload_to='ekstraksi/', blank=False, null=False)
	waktu = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.id

	def namagambar(self):
		return nama_gambar(self.gambar.name)

	class Meta:
		ordering = ['-waktu']


class AktivitasPengguna(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	is_online = models.BooleanField(default=False)

	def make_online(self):
		self.is_online = True
		self.save()

	def make_offline(self):
		self.is_online = False
		self.save()