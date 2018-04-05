from utils import log
from models import User
from objects import Response
from utils import random_str
import time

# 服务器端保存的客户的信息
user_info = {}


def route_static(request):
	resp = Response()
	resp.add_header("Content-Type", "image/jpeg")
	filename = request.query().get("file", "1.jpg")
	with open("static/" + filename, "rb") as f:
		resp.body = f.read()
	return resp


def template(filename):
	with open(filename, encoding="utf-8") as f:
		return f.read()


def route_page(request):
	resp = Response()
	resp.add_header("Content-Type", "text/html; charset=UTF-8")
	resp.body = template("templates\\1.html").encode("utf-8")
	return resp


def route_index(request):
	resp = Response()
	resp.add_header("Content-Type", "text/html; charset=UTF-8")
	body = template("templates\\index.html")
	# 验证是否登陆
	user = request.validate_login(user_info)
	if user is not None:
		body = body.replace("{{user}}", user)
	body = body.replace("{{user}}", "SomeBody")
	resp.body = body.encode("utf-8")
	return resp


def route_login(request):
	resp = Response()
	resp.add_header("Content-Type", "text/html; charset=UTF-8")
	if request.method == "POST":
		form = request.form()
		user = User.new(form)
		if user.validate_login():
			s = random_str()
			user_info[s] = {
				"username": user.username,
				"expires": time.time()
			}
			cookie = "Session-Id={}".format(s)
			resp.add_header("Set-Cookie", cookie)
			body = template("templates\\success.html").replace("{{user}}", user.username)
		else:
			body = template("templates\\loginForm.html").replace("{{message}}", "您的用户名或密码不正确")
	else:
		body = template("templates\\loginForm.html").replace("{{message}}", "")
	resp.body = body.encode("utf-8")
	return resp


def route_register(request):
	resp = Response()
	resp.add_header("Content-Type", "text/html; charset=UTF-8")
	if request.method == "POST":
		form = request.form()
		user = User.new(form)
		if user.validate_register():
			user.save()
			body = template("templates\\success.html").replace("{{user}}", user.username)
		else:
			body = template("templates\\registerForm.html").replace("{{message}}", "注册失败")
	else:
		body = template("templates\\registerForm.html").replace("{{message}}", "")
	resp.body = body.encode("utf-8")
	return resp


def error(request, error_code=404):
	resp = Response()
	resp.status = error_code
	resp.description = "Not Found"
	e = {
		404: b"<h1>NOT FOUND</h1>"
	}
	resp.body = e.get(error_code)
	return resp


routes_dict = {
	"/": route_index,
	"/index": route_index,
	"/static": route_static,
	"/login": route_login,
	"/register": route_register,
	"/1.html": route_page,
}
