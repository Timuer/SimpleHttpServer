# coding: utf-8

import socket
from utils import log

def parsed_request(request):
	parts = request.split("\r\n\r\n")
	if len(parts) == 1:
		head = parts[0]
		if not head.strip():
			raise RuntimeError("Empty Request")
		body = ""
	else:
		head = parts[0]
		body = parts[1]
	return head, body

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

def dispatch_req_by_path(path):
	dispatch_dict = {
		"/": route_index,
		"/1.jpg": route_image,
	}
	route_func = dispatch_dict.get(path, error)
	return route_func()

def page(filename):
	with open(filename, encoding="utf-8") as f:
		return f.read()

def route_page():
	header = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n"
	body = page("page\\1.html")
	content = header + "\r\n" + body
	return content.encode("utf-8")

def route_index():
	header = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n"
	body = "<h1>Hello World</h1><img src='/1.jpg'>"
	content = header + "\r\n" + body
	return content.encode("utf-8")

def route_image():
	header = b"HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n"
	with open("img\\1.jpg", "rb") as img:
		content = header + b"\r\n" + img.read()
	return content

def error(error_code=404):
	e = {
		404: b"HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>"
	}
	return e.get(error_code)

def start_server(host="", port=8000):
	with socket.socket() as s:
		s.bind((host, port))

		while True:
			s.listen(5)
			# accept函数在接收到http请求之前不会返回，该线程会阻塞在这里
			connection, address = s.accept()
			request = request_by_socket(connection).decode("UTF-8")
			try:
				# 解析请求
				head, body = parsed_request(request)
				head_info = parsed_request_head(head)

				# 根据请求路径路由到相应处理函数
				path = head_info["path"]
				response = dispatch_req_by_path(path)
				connection.sendall(response)
			except Exception as e:
				log("error", e)
			connection.close()

def main():
	config = dict(
		host = "",
		port = 8000,
	)
	start_server(**config)

if __name__=="__main__":
	main()


