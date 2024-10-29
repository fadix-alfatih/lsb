import numpy as np

def kualitas_hasil(asli, hasil):
	mse = np.mean((asli - hasil) ** 2)
	if mse == 0:
		return 100, 0
	else:
		max_pixel_value = 255.0
		psnr = 20 * np.log10(max_pixel_value / np.sqrt(mse))
		return mse, psnr