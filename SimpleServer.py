# coding: utf-8

import socket
from utils import log
from objects import Request
from routes import routes_dict
from todo_routes import routes_todo_dict
from routes import error
import _thread


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
	request.info = head_info
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


def dispatch_request(request):
	dispatch_dict = update_dispatches()
	route_func = dispatch_dict.get(request.short_path(), error)
	return route_func(request)


def update_dispatches():
	dispatch_dict = {}
	for d in routes_list:
		dispatch_dict.update(d)
	return dispatch_dict


routes_list = [
	routes_dict,
	routes_todo_dict,
]


def process_response(connection):
	try:
		request_data = request_by_socket(connection).decode("UTF-8")
		# 解析请求，生成请求对象
		request = parsed_request(request_data)
		# 传递请求对象，由该函数分发到相应处理函数
		response = dispatch_request(request)
		connection.sendall(response.data())
	except Exception as e:
		log("error", e)
	connection.close()

def start_server(host="", port=80):
	with socket.socket() as s:
		s.bind((host, port))
		while True:
			s.listen(5)
			# accept函数在接收到http请求之前不会返回，该线程会阻塞在这里
			connection, address = s.accept()
			log("connect address: ", address)
			_thread.start_new_thread(process_response, (connection,))


def main():
	config = dict(
		host="",
		port=8000,
	)
	start_server(**config)


if __name__ == "__main__":
	main()
