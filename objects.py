import urllib.parse



class Request(object):
	def __init__(self):
		self.method = "GET"
		self.path = ""
		self.body = ""
		self.info = {}

	# 获取请求体中的表单参数
	def form(self):
		pairs = self.body.split("&")
		params = {}
		for pair in pairs:
			# 将客户端使用编码转义的特殊字符还原
			pair = urllib.parse.unquote(pair)
			key, value = pair.split("=")
			params[key] = value
		return params

	# 获取路径中的参数
	def query(self):
		index = self.path.find("?")
		if index == -1:
			return {}
		else:
			query_str = self.path[index + 1:]
			pairs = query_str.split("&")
			params = {}
			for pair in pairs:
				# 将客户端使用编码转义的特殊字符还原
				pair = urllib.parse.unquote(pair)
				key, value = pair.split("=")
				params[key] = value
			return params

	def short_path(self):
		return self.path.split("?")[0]

	def cookies(self):
		cookies = {}
		c = self.info.get("Cookie", "")
		if c is not "":
			pairs = c.split(";")
			for pair in pairs:
				k, v = pair.split("=")
				cookies[k.strip()] = v.strip()
		return cookies


class Response(object):
	def __init__(self):
		self.status = 200
		self.description = "OK"
		self.headers = {}
		self.body = b""

	def add_header(self, key, value):
		self.headers[key] = value

	def add_headers(self, **kwargs):
		for k, v in kwargs.items():
			self.headers[k] = v

	def data(self):
		status_line = "HTTP/1.1 {} {}\r\n".format(str(self.status), self.description)
		headers = ""
		for k, v in self.headers.items():
			headers += "{}: {}\r\n".format(k, v)
		head = status_line + headers
		content = head.encode("utf-8") + b"\r\n" + self.body
		return content
