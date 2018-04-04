import random



def log(*args, **kwargs):
	print("log", args, kwargs)


def random_str():
	s = "alsdkfjasldfkjiennvoihwenflknv"
	result = ""
	for i in range(10):
		index = random.randint(0, len(s) - 2)
		result += s[index]
	return result