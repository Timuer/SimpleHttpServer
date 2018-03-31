import socket


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
	head_info["protocal"] = command_line.split()[0].split("/")[0]
	head_info["version"] = command_line.split()[0].split("/")[1]
	head_info["status"] = command_line.split()[1]
	head_info["information"] = " ".join(command_line.split()[2:])
	for line in headers:
		key = line.split(":")[0].strip()
		value = line.split(":")[1:]
		if len(value) > 1:
			value = ":".join(value).strip()
		else:
			value = value[0].strip()
		head_info[key] = value
	return head_info



if __name__=="__main__":
	# 创建套接字
	s = socket.socket()

	host = "g.cn"
	port = 80
	# 连接到主机
	s.connect((host, port))

	http_request = "GET / HTTP/1.1\r\nhost: {}\r\n\r\n".format(host)
	request = http_request.encode(encoding="UTF-8")
	# 发送请求
	s.send(request)

	r = b''
	buffer_size = 1024
	while True:
		buffer = s.recv(buffer_size)
		r += buffer
		if len(buffer) < buffer_size:
			break

	response = r.decode("utf-8")
	head_info, html = parsed_response(response)
	print(head_info, html)