# coding: utf-8

import socket
import ssl

def parsed_url(url):
	protocol = "http"
	host = ""
	port = 80
	path = "/"
	query = ""

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

		# 解析路径和参数
		tmp = tmp[i:]
		i = tmp.find("?")
		if i == -1:
			path = tmp
		else:
			path = tmp[:i]
			query = tmp[i + 1:]

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
		"query": query,
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

def get(url):
	url_info = parsed_url(url)
	# 创建套接字
	s = create_socket(url_info["protocol"])

	# 创建HTTP请求报文
	user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
	referer = "https://movie.douban.com/"
	http_data = "GET {} HTTP/1.1\r\nhost: {}\r\nConnection: close\r\nUser-Agent: {}\r\nReferer: {}\r\n\r\n"
	http_request = http_data.format(url_info["path"], url_info["host"], user_agent, referer)

	# 连接到主机
	s.connect((url_info["host"], url_info["port"]))
	s.send(http_request.encode("utf-8"))

	# 接收和解析响应
	resp = response_by_socket().decode("utf-8")
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
	head_info, html = get("https://movie.douban.com/chart")
	print(head_info, html)