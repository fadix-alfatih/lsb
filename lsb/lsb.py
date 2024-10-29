from lsb.const import MESSAGE_END_DELIMITER

class LeastSignificantBit:
	"""docstring for LSB"""

	def sisip(gambar, pesan):
		width, height = gambar.shape
		msg_bits = pesan
		img = gambar.flatten()
		for index, bit in enumerate(msg_bits):
			value = img[index]
			value = bin(value)
			value = value[:-1] + bit
			img[index] = int(value, 2)
		img = img.reshape(width, height)
		return img

	def ekstrak(gambar):
		img = gambar.flatten()
		msg = ''
		index = 0
		while msg[-len(MESSAGE_END_DELIMITER):] != MESSAGE_END_DELIMITER:
			bits = [bin(i)[-1] for i in img[index:index+8]]
			bits = ''.join(bits)
			try:
				msg += chr(int(bits, 2))
			except ValueError as e:
				pass
			index += 8
			if index > img.shape[0]:
				retrived = 'Tidak ada pesan!'
				break
		retrived = msg
		return retrived