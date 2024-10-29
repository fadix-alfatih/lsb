from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth

from lsb.calculate import kualitas_hasil
from lsb.forms import *
from lsb.functions import semua_user, data_model, make_user_offline, make_user_online
from lsb.functions import pesan_validasi_gambar, proses_pesan, proses_hasil_ekstrak
from lsb.auto import buat_id
from lsb.models import Penyisipan, Ekstraksi, AktivitasPengguna
from lsb.stego import sisip_gambar_pesan, ekstrak_pesan_gambar, preproses_gambar
from lsb.validators import *

from io import BytesIO
from pathlib import Path

# Create your views here.
def dashboard(request):
	if not request.user.is_authenticated:
		return redirect('signin')
	make_user_online(AktivitasPengguna, request.user)

	halaman = 'dashboard'

	if request.user.is_superuser:
		data = data_model(Penyisipan), data_model(Ekstraksi)
	else:
		data = data_model(Penyisipan, request.user), data_model(Ekstraksi, request.user)
	
	context = {
		'halaman': halaman,
		'data': data,
	}
	template = f'main/{halaman}.html'
	return render(request, template, context)


def penyisipan(request):
	if not request.user.is_authenticated:
		return redirect('signin')
	make_user_online(AktivitasPengguna, request.user)

	halaman = 'penyisipan'
	completed = False
	myid = None

	if request.method == 'POST':
		form = FormPenyisipan(request.POST, request.FILES)
		if form.is_valid():
			data = {
				'user': request.user,
				'gambar': form.cleaned_data.get('gambar'),
				'pesan': form.cleaned_data.get('pesan'),
				}
			if validasi_gambar(data['gambar']):
				prehasil, maximal = preproses_gambar(data['gambar'])
				if validasi_penyisipan(prehasil):
					data['pesan'] = proses_pesan(data['pesan'])
					if validasi_panjang_pesan(data['pesan'], maximal):
						sisip, akhir = sisip_gambar_pesan(prehasil, data['pesan'])
						mse, psnr = kualitas_hasil(prehasil, sisip)
						# print(mse, psnr)

						buffer = BytesIO()
						akhir.save(buffer, format='PNG')

						myid = buat_id(Penyisipan)

						myData = form.save(commit=False)
						myData.id = myid
						myData.user = data['user']
						myData.mse = mse
						myData.psnr = psnr
						myData.nama = Path(myData.gambar.name).name
						myData.save()
						myData.gambar.save(data['gambar'].name, BytesIO(buffer.getvalue()))
						buffer.close()

						completed = True
						messages.success(request, 'Pesan berhasil disisipkan')
					else:
						messages.error(request, 'Penyisipan gagal, pesan terlalu panjang')
				else:
					messages.error(request, 'Penyisipan gagal, terdapat pesan yang telah disisipkan')
			else:
				messages.error(request, f'Hanya {pesan_validasi_gambar()}')
	else:
		form = FormPenyisipan()

	context = {
		'halaman': halaman,
		'form': form,
		'completed': completed,
		'myid': myid,
	}
	template = f'main/{halaman}.html'
	return render(request, template, context)


def ekstraksi(request):
	if not request.user.is_authenticated:
		return redirect('signin')
	make_user_online(AktivitasPengguna, request.user)

	print('halaman ekstraksi')

	halaman = 'ekstraksi'
	completed = False
	hasil = None

	if request.method == 'POST':
		form = FormEkstraksi(request.POST, request.FILES)
		if form.is_valid():
			gambar = form.cleaned_data.get('gambar')
			if validasi_gambar(gambar):
				prehasil, _ = preproses_gambar(gambar)
				ekstrak = ekstrak_pesan_gambar(prehasil)
				pesan = proses_hasil_ekstrak(ekstrak)
				if pesan:
					myData = form.save(commit=False)
					myData.id = buat_id(Ekstraksi)
					myData.user = request.user
					myData.nama = gambar.name
					myData.gambar = gambar
					myData.save()

					completed = True
					hasil = pesan
					messages.success(request, 'Pesan berhasil diekstrak')
			else:
				messages.error(request, f'Hanya {pesan_validasi_gambar()}')

	else:
		form = FormEkstraksi()

	context = {
		'halaman': halaman,
		'form': form,
		'completed': completed,
		'hasil': hasil,
	}
	template = f'main/{halaman}.html'
	return render(request, template, context)


def aktivitas(request):
	if not request.user.is_authenticated:
		return redirect('signin')
	make_user_online(AktivitasPengguna, request.user)

	halaman = 'aktivitas'
	model_penyisipan, model_ekstraksi = None, None

	if request.user.is_superuser:
		model_penyisipan = Penyisipan.objects.all()
		model_ekstraksi = Ekstraksi.objects.all()
	else:
		model_penyisipan = Penyisipan.objects.filter(user=request.user)
		model_ekstraksi = Ekstraksi.objects.filter(user=request.user)

	context = {
		'halaman': halaman,
		'model_penyisipan': model_penyisipan,
		'model_ekstraksi': model_ekstraksi,
	}
	template = f'main/{halaman}.html'
	return render(request, template, context)


def detailstegano(request, marker, uid):
	if not request.user.is_authenticated:
		return redirect('signin')
	make_user_online(AktivitasPengguna, request.user)

	halaman = marker
	state = 'detail'
	subhalaman = 'stegano'

	data = None
	if marker == 'penyisipan':
		data = get_object_or_404(Penyisipan, id=uid)
	elif marker == 'ekstraksi':
		data = get_object_or_404(Ekstraksi, id=uid)
	else:
		return redirect('aktivitas')

	context = {
		'halaman': halaman,
		'state': state,
		'uid': uid,
		'marker': marker,
		'data': data,
	}
	template = f'main/{state}-{subhalaman}.html'
	return render(request, template, context)


def unduh(request, marker, uid):
	if not request.user.is_authenticated:
		return redirect('signin')
	make_user_online(AktivitasPengguna, request.user)

	model = None
	if marker == 'penyisipan':
		model = Penyisipan
	elif marker == 'penyisipan':
		model = Ekstraksi
	else:
		return redirect('detail', marker, uid)

	data = get_object_or_404(model, id=uid)
	response = HttpResponse(data.gambar, content_type='application/force-download')
	response['Content-Disposition'] = f'attachment; filename="{data.namagambar()}"'
	return response


def hapus(request, marker, uid):
	if not request.user.is_authenticated:
		return redirect('signin')
	make_user_online(AktivitasPengguna, request.user)

	model = None
	if marker == 'penyisipan':
		model = Penyisipan
	elif marker == 'penyisipan':
		model = Ekstraksi
	else:
		return redirect('aktivitas')

	data = get_object_or_404(model, id=uid)
	if data.delete():
		messages.success(request, 'Data berhasil dihapus')
	else:
		messages.error(request, 'Data gagal dihapus')
	return redirect('aktivitas')


def hapuspengguna(request, usn):
	if not request.user.is_authenticated:
		return redirect('signin')

	data = get_object_or_404(model, username=usn)
	if data.delete():
		messages.success(request, 'Pengguna berhasil dihapus')
	else:
		messages.error(request, 'Pengguna gagal dihapus')
	return redirect('pengguna')


def langkah(request, marker, uid):
	if not request.user.is_authenticated:
		return redirect('signin')
	make_user_online(AktivitasPengguna, request.user)

	halaman = 'langkah'
	context = {
		'halaman': halaman,
	}
	template = f'main/{halaman}.html'
	return render(request, template, context)


def pengguna(request):
	if not request.user.is_authenticated:
		return redirect('signin')
	make_user_online(AktivitasPengguna, request.user)

	halaman = 'pengguna'
	context = {
		'halaman': halaman,
		'pengguna': semua_user(),
	}
	template = f'main/{halaman}.html'
	return render(request, template, context)


def detailpengguna(request, usn):
	# print('ok')
	if not request.user.is_authenticated:
		return redirect('signin')
	make_user_online(AktivitasPengguna, request.user)

	data = get_object_or_404(User, username=usn)

	halaman = 'pengguna'
	state = 'detail'
	subhalaman = 'pengguna'
	context = {
		'halaman': halaman,
		'uid': usn,
		'data': data,
	}
	template = f'main/detail-pengguna.html'
	return render(request, template, context)


def profil(request):
	if not request.user.is_authenticated:
		return redirect('signin')
	make_user_online(AktivitasPengguna, request.user)

	halaman = 'profil'
	context = {
		'halaman': halaman,
	}
	template = f'main/{halaman}.html'
	return render(request, template, context)

'''
=================================AUTH=====================================
'''

def signin(request):
	halaman = 'signin'

	if request.method == 'POST':
		form = FormSignIn(request.POST, request.FILES)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')

			user = auth.authenticate(username=username, password=password)
			if user is not None:
				try:
					auth.login(request, user)
					AktivitasPengguna.objects.get(user=user).make_online()
					return redirect('dashboard')
				except Exception as e:
					return redirect('login')
			else:
				messages.error(request, 'Login gagal')
				return redirect('signin')
	else:
		form = FormSignIn()

	context = {
		'halaman': halaman,
		'form': form,
	}
	template = f'auth/{halaman}.html'
	return render(request, template, context)


def signout(request):
	if not request.user.is_authenticated:
		return redirect('signin')
	try:
		make_user_offline(AktivitasPengguna, request.user)
		auth.logout(request)
		return redirect('signin')
	except Exception as e:
		return ('dashboard')


def daftar(request):
	halaman = 'daftar'

	if request.method == 'POST':
		form = FormDaftar(request.POST, request.FILES)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			passwordconf = form.cleaned_data.get('passwordconf')
			status, pesan = validasi_daftar(email, username, password, passwordconf)
			if status:
				messages.success(request, pesan)
			else:
				messages.error(request, pesan)
	else:
		form = FormDaftar()

	context = {
		'halaman': halaman,
		'form': form,
	}
	template = f'auth/{halaman}.html'
	return render(request, template, context)