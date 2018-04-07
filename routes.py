from utils import log
from models import User
from objects import Response
from utils import random_str
import time
from jinja2 import Environment, FileSystemLoader
import os.path
from utils import encrypted_password


path = "{}/templates/".format(os.path.dirname(__file__))
loader = FileSystemLoader(path)
env = Environment(loader=loader)


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
	filename = request.query().get("file", "")
	path = ""
	if filename.endswith(".jpg"):
		resp.add_header("Content-Type", "image/jpeg")
		path = "static/img/" + filename
	elif filename.endswith(".js"):
		resp.add_header("Content-Type", "application/javascript")
		path = "static/js/" + filename
	elif filename.endswith(".css"):
		resp.add_header("Content-Type", "text/css")
		path = "static/css/" + filename
	with open(path, "rb") as f:
		resp.body = f.read()
	return resp


def route_page(request):
	resp = Response()
	resp.add_header("Content-Type", "text/html; charset=UTF-8")
	resp.body = env.get_template("1.html").render().encode("utf-8")
	return resp


def route_index(request):
	resp = Response()
	resp.add_header("Content-Type", "text/html; charset=UTF-8")
	tmp = env.get_template("index.html")
	user = request.validate_login(cookie_info)
	if user:
		tmp = tmp.render(user=user.username)
	else:
		tmp = tmp.render(user="【游客】")
	resp.body = tmp.encode("utf-8")
	return resp


def route_login(request):
	resp = Response()
	resp.add_header("Content-Type", "text/html; charset=UTF-8")
	if request.method == "POST":
		form = request.form()
		user_form = User.new(form)
		user_form.password = encrypted_password(user_form.password)
		user = user_form.validate_login()
		if user:
			s = random_str()
			cookie_info[s] = {
				"userid": user.id,
				"expires": time.time()
			}
			cookie = "Session-Id={}".format(s)
			resp.add_header("Set-Cookie", cookie)
			tmp = env.get_template("success.html").render(user=user.username)
		else:
			tmp = env.get_template("loginForm.html").render(message="您的用户名或密码不正确")
	else:
		tmp = env.get_template("loginForm.html").render(message="")
	resp.body = tmp.encode("utf-8")
	return resp


def route_register(request):
	resp = Response()
	resp.add_header("Content-Type", "text/html; charset=UTF-8")
	if request.method == "POST":
		form = request.form()
		user_form = User.new(form)
		user_form.password = encrypted_password(user_form.password)
		if user_form.validate_register():
			user_form.save()
			tmp = env.get_template("success.html").render(user=user_form.username)
		else:
			tmp = env.get_template("registerForm.html").render(message="注册失败")
	else:
		tmp = env.get_template("registerForm.html").render(message="")
	resp.body = tmp.encode("utf-8")
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
