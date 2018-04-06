from utils import log
from models import User
from objects import Response
from utils import random_str
import time

# 服务器端保存的客户的信息
cookie_info = {}

def login_required(func):
	def real_route(request):
		if request.validate_login(cookie_info):
			return func(request)
		else:
			return redirect("/index")
	return real_route


def redirect(url):
	response = Response()
	response.status = 302
	response.add_header("Location", url)
	return response


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
	user = request.validate_login(cookie_info)
	if user:
		body = body.replace("{{user}}", user.username)
	else:
		body = body.replace("{{user}}", "【游客】")
	resp.body = body.encode("utf-8")
	return resp


def route_login(request):
	resp = Response()
	resp.add_header("Content-Type", "text/html; charset=UTF-8")
	if request.method == "POST":
		form = request.form()
		user_form = User.new(form)
		user = user_form.validate_login()
		if user:
			s = random_str()
			cookie_info[s] = {
				"userid": user.id,
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
		user_form = User.new(form)
		if user_form.validate_register():
			log("validate ok")
			user_form.save()
			body = template("templates\\success.html").replace("{{user}}", user_form.username)
		else:
			log("validate fail")
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
