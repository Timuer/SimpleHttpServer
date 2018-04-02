from utils import log

def template(filename):
	with open(filename, encoding="utf-8") as f:
		return f.read()

def route_page(request):
	header = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n"
	body = template("templates\\1.html")
	content = header + "\r\n" + body
	return content.encode("utf-8")

def route_index(request):
	header = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n"
	user = request.query().get("user")
	body = template("templates\\index.html")
	content = header + "\r\n" + body
	if user:
		content = content.replace("{{user}}", user)
	else:
		content = content.replace("{{user}}", "SomeBody")
	return content.encode("utf-8")

# def route_image(request):
# 	header = b"HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n"
# 	with open("img\\1.jpg", "rb") as img:
# 		content = header + b"\r\n" + img.read()
# 	return content

def route_static(request):
	header = b"HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n"
	filename = request.query().get("file", "1.jpg")
	with open("static/" + filename, "rb") as f:
		content = header + b"\r\n" + f.read()
	return content

def route_login(request):
	header = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n"
	if request.method == "POST":
		form = request.form()
		user = form.get("user")
		password = form.get("password")
		if user and password:
			if user == "tianmu" and password == "12345":
				body = template("templates\\index.html").replace("{{user}}", user)
			else:
				body = template("templates\\loginForm.html")
		else:
			body = template("templates\\loginForm.html")
	else:
		body = template("templates\\loginForm.html")
	content = header + "\r\n" + body
	return content.encode("utf-8")

def route_register(request):
	pass

def error(request, error_code=404):
	e = {
		404: b"HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>"
	}
	return e.get(error_code)

def dispatch_request(request):
	# 通过不带参数的路径映射到处理函数
	route_func = dispatch_dict.get(request.short_path(), error)
	return route_func(request)

dispatch_dict = {
	"/": route_index,
	# "/1.jpg": route_image,
	"/static": route_static,
	"/login": route_login,
	"/register": route_register,
	"/1.html": route_page,
}