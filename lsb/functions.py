from django.contrib.auth.models import User
from django.utils import timezone

from lsb.const import ALLOWED_IMAGE_EXTENSION, MAX_DATA, MESSAGE_START_DELIMITER, MESSAGE_END_DELIMITER
from lsb.auto import buat_id

def nama_gambar(nama):
	nama = nama.split('/')[-1]
	return nama

def buat_user_baru(email, username, password):
	status, msg = False, None
	user = User.objects.create_user(
		email=email,
		username=username,
		password=password,
		)
	if user is not None:
		status = True
		msg = f'{username} berhasil dibuat'
	else:
		status = False
		msg = 'Akun gagal ditambahkan'
	return status, msg

def semua_user():
	return User.objects.all()

def data_model(model, user=None):
	total, data = None, None
	today = timezone.now().date()
	if user is None:
		# print('superuser')
		total = model.objects.count()

		num = MAX_DATA if total > MAX_DATA else total
		now = model.objects.filter(waktu=today).count()
		data = model.objects.all().order_by('-waktu')[:num]
	else:
		# print('user')
		total = model.objects.filter(user=user).count()

		num = MAX_DATA if total > MAX_DATA else total
		now = model.objects.filter(user=user, waktu=today).count()
		data = model.objects.all().order_by('-waktu')[:num]
	return total, now, data

def pesan_validasi_gambar():
	return ', '.join(str(x)[1:] for x in ALLOWED_IMAGE_EXTENSION)

def make_user_offline(model, user):
	model.objects.get(user=user).make_offline()

def make_user_online(model, user):
	model.objects.get(user=user).make_online()

def proses_pesan(pesan):
	secret = MESSAGE_START_DELIMITER + pesan + MESSAGE_END_DELIMITER
	secret = secret.encode('ascii')
	secret = ''.join([format(i,'08b') for i in secret])
	return secret

def proses_hasil_ekstrak(pesan):
	# pesan = pesan.split(MESSAGE_START_DELIMITER, 1)
	hasil = pesan.split(MESSAGE_END_DELIMITER)[0]
	hasil = hasil.split(MESSAGE_START_DELIMITER)[1]
	return hasil