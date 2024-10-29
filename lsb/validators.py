from django.contrib.auth.models import User

from lsb.functions import buat_user_baru, proses_hasil_ekstrak
from lsb.const import *
from lsb.auto import *
from lsb.stego import ekstrak_pesan_gambar

import os

def validasi_daftar(email, username, password, passwordconf):
	status, msg = False, None
	if password == passwordconf:
		if not User.objects.filter(username=username).exists():
			status, msg = buat_user_baru(email, username, password)
		else:
			status = False
			msg = f'{username} telah terdaftar, silahkan login'
	else:
		status = False
		msg = 'Password tidak sama!'
	return status, msg

def validasi_gambar(gambar):
	nama, ekstensi = os.path.splitext(gambar.name)
	if ekstensi.lower() in ALLOWED_IMAGE_EXTENSION:
		return True
	else:
		return False

def validasi_panjang_pesan(pesan, gambar):
	if len(pesan) > gambar.size:
		return False
	else:
		return True

def validasi_penyisipan(gambar):
	ekstrak = ekstrak_pesan_gambar(gambar)
	try:
		hasil = proses_hasil_ekstrak(ekstrak)
		return False
	except:
		return True 