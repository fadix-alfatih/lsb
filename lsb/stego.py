from lsb.lsb import LeastSignificantBit as lsb

from PIL import Image

import numpy as np

def sisip_gambar_pesan(gambar, pesan):
	sisip = lsb.sisip(gambar, pesan)
	hasil = Image.fromarray(sisip)
	return sisip, hasil

def ekstrak_pesan_gambar(gambar):
	ekstrak = lsb.ekstrak(gambar)
	return ekstrak

def preproses_gambar(gambar):
	grayscale = Image.open(gambar).convert('L')
	hasil = np.array(grayscale)
	maximal = np.array(list(grayscale.getdata()))
	return hasil, maximal