from lsb.const import MAX_LENGTH_ID

import string, secrets

def id():
	myid = string.digits + string.ascii_letters
	return ''.join(secrets.choice(myid) for _ in range(MAX_LENGTH_ID))

def buat_id(model):
	myid = id()
	while model.objects.filter(id=myid).exists():
		myid = id()
	return myid