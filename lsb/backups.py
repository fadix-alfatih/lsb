
def buat_data_baru(model, data):
	myid = buat_id(model)
	try:
		instance = model.objects.create(
			id=myid,
			user=data['user'],
			nama=data['gambar'].name,
			gambar=data['gambar'],
			)
		if instance is not None:
			return True
		else:
			return False
	except Exception as e:
		return False