# coding: utf-8

import socket

def parsed_request_head(head):
	command_line = head.split("\r\n")[0]
	headers = head.split("\r\n")[1:]
	head_info = {}
	head_info["method"] = command_line.split()[0]
	head_info["path"] = command_line.split()[1]
	head_info["protocal"] = command_line.split()[2].split("/")[0]
	head_info["version"] = command_line.split()[2].split("/")[1]
	for line in headers:
		key = line.split(":")[0].strip()
		value = line.split(":")[1].strip()
		head_info[key] = value
	return head_info

if __name__=="__main__":
	s = socket.socket()

	host = ""
	port = 8000

	s.bind((host, port))

	while True:
		s.listen(5)
		# accept函数在接收到http请求之前不会返回，该线程会阻塞在这里
		connection, address = s.accept()
		r = b''
		while True:
			buffer_size = 1024
			buffer = connection.recv(buffer_size)
			if len(buffer) < 1024:
				break
			r += buffer
		request = r.decode("UTF-8")

		head = request.split("\r\n\r\n")[0]
		body = request.split("\r\n\r\n")[1]
		head_info = parsed_request_head(head)
		print(address, head_info, body)

		response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n<h1>Hello World</h1>"
		connection.sendall(response.encode(encoding="UTF-8"))


