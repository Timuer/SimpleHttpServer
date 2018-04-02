# coding: utf-8

import socket
import ssl
from utils import log

class Request(object):
	def __init__(self):
		self.method = "GET"
		self.path = "/"
		self.port = 80
		self.protocol = "http"
		self.headers = {}
		self.body = ""

	def set_request(self, url):
		info = parsed_url(url)
		self.path = info["path"]
		self.port = info["port"]
		self.protocol = info["protocol"]
		self.host = info["host"]
		self.add_header("host", info["host"])
		self.add_header("Connection", "close")

	def add_header(self, key, value):
		self.headers[key] = value

	def get_header(self, key):
		return self.headers.get(key)

	def data(self):
		data = self.method + " " + self.path + " " + "HTTP/1.1\r\n"
		for k, v in self.headers.items():
			line = k + ": " + v + "\r\n"
			data += line
		content = data + "\r\n" + self.body
		return content.encode("utf-8")



def parsed_url(url):
	protocol = "http"
	host = ""
	port = 80
	path = "/"

	# 解析http协议
	if url.startswith("https"):
		protocol = "https"

	# 解析主机名
	tmp = url.split("://")[1]
	i = tmp.find("/")
	if i == -1:
		host = tmp
		path = "/"
	else:
		host = tmp[:i]

	# 解析端口
	port_dict = {
		"http": 80,
		"https": 443,
	}
	port = port_dict[protocol]
	if ":" in host:
		h = host.split(":")
		host = h[0]
		port = int(h[1])

	return {
		"protocol": protocol,
		"host": host,
		"port": port,
		"path": path,
	}


def parsed_response(resp):
	parts = resp.split("\r\n\r\n")
	if len(parts) == 1:
		head = parts[0]
		body = ""
	else:
		head = parts[0]
		body = parts[1]
	return parsed_response_head(head), body

def parsed_response_head(head):
	command_line = head.split("\r\n")[0]
	headers = head.split("\r\n")[1:]
	head_info = {}
	head_info["status"] = int(command_line.split()[1])

	for line in headers:
		key = line.split(":")[0].strip()
		value = line.split(":")[1:]
		if len(value) > 1:
			value = ":".join(value).strip()
		else:
			value = value[0].strip()
		head_info[key] = value
	return head_info


def create_request(url):
	request = Request()
	request.set_request(url)
	return request

def get(request):

	# 创建套接字
	s = create_socket(request.protocol)

	# 创建HTTP请求报文
	user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
	referer = "https://movie.douban.com/"
	request.add_header("User-Agent", user_agent)
	request.add_header("referer", referer)

	# 连接到主机
	s.connect((request.host, request.port))
	log(request.data())
	s.send(request.data())

	# 接收和解析响应
	resp = response_by_socket(s).decode("utf-8")
	resp_info, html =  parsed_response(resp)

	# 处理重定向
	if resp_info["status"] in [301, 302]:
		return get(resp_info["Location"])

	return resp_info, html

def create_socket(protocol):
	s = socket.socket()
	if protocol == "https":
		s = ssl.wrap_socket(s)
	return s

def response_by_socket(sock):
	r = b''
	buffer_size = 1024
	while True:
		buffer = sock.recv(buffer_size)
		r += buffer
		if len(buffer) < buffer_size:
			break
	return r

if __name__=="__main__":
	r = create_request("https://movie.douban.com/chart")
	head_info, html = get(r)
	print(head_info, html)