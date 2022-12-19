import bcrypt


def hash_password(password):
	return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

def verify_password(password, hashed_password):
	return bcrypt.checkpw(password.encode('utf8'), hashed_password)