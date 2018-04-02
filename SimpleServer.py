# coding: utf-8

import socket
from utils import log
import urllib.parse
from routes import dispatch_request

class Request(object):
	def __init__(self):
		self.method = "GET"
		self.path = ""
		self.body = ""

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
			query_str = self.path[index+1:]
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

def parsed_request(request_data):
	parts = request_data.split("\r\n\r\n")
	request = Request()
	if len(parts) == 1:
		head = parts[0]
		if not head.strip():
			raise RuntimeError("Empty Request")
		body = ""
	else:
		head = parts[0]
		body = parts[1]
	head_info = parsed_request_head(head)
	request.path = head_info["path"]
	request.method = head_info["method"]
	request.body = body
	return request

def parsed_request_head(head):
	command_line = head.split("\r\n")[0]
	headers = head.split("\r\n")[1:]
	head_info = {}
	head_info["method"] = command_line.split()[0]
	head_info["path"] = command_line.split()[1]
	for line in headers:
		key = line.split(":")[0].strip()
		value = line.split(":")[1].strip()
		head_info[key] = value
	return head_info

def request_by_socket(sock):
	r = b''
	buffer_size = 1024
	while True:
		buffer = sock.recv(buffer_size)
		r += buffer
		if len(buffer) < 1024:
			break
	return r

def start_server(host="", port=8000):
	with socket.socket() as s:
		s.bind((host, port))
		while True:
			s.listen(5)
			# accept函数在接收到http请求之前不会返回，该线程会阻塞在这里
			connection, address = s.accept()
			log("connect address: ", address)
			try:
				request_data = request_by_socket(connection).decode("UTF-8")
				log(request_data)
				# 解析请求，生成请求对象
				request = parsed_request(request_data)
				# 传递请求对象，由该函数分发到相应处理函数
				response = dispatch_request(request)
				connection.sendall(response)
			except Exception as e:
				log("error", e)
				continue
			connection.close()

def main():
	config = dict(
		host = "",
		port = 8000,
	)
	start_server(**config)

if __name__=="__main__":
	main()


