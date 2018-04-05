from objects import Response
from routes import template
from routes import user_info
from models import Todo
from utils import log



def routes_todo(request):
	resp = Response()
	body = template("templates\\todo_index.html")
	user = request.validate_login(user_info)
	if user is not None:
		lst = Todo.find_by(userid=user.id)
		if lst:
			todos = lst[0].todos
			s = ""
			for item in todos:
				edit_url = "/todo/edit?id={}".format(item.get("itemid"))
				del_url = "/todo/del?id={}".format(item.get("itemid"))
				s += "<li>{}<a href='{}'>编辑</a><a href='{}'>删除</a></li>".format(item.get("title"), edit_url, del_url)
			resp.body = body.replace("{{todos}}", s).encode("utf-8")
		else:
			resp.body = body.replace("{{todos}}", "您还没有添加todo，快来添加吧").encode("utf-8")
	else:
		resp.set_redirect("/login")
	return resp


def routes_add(request):
	resp = Response()
	if request.method == "POST":
		user = request.validate_login(user_info)
		form = request.form()
		title = form.get("title")
		if user is not None:
			lst = Todo.find_by(userid=user.id)
			if lst == []:
				todo = Todo.new({
					"userid": user.id,
				})
			else:
				todo = lst[0]
			if todo.todos:
				i = len(todo.todos)
				todo_item = {
					"itemid": i + 1,
					"title": title,
				}
				todo.todos.append(todo_item)
			else:
				todo_item = {
					"itemid": 1,
					"title": title,
				}
				todo.todos = [todo_item]
			todo.del_by(userid=user.id)
			todo.save()
			resp.set_redirect("/todo")
	return resp


def routes_edit(request):
	resp = Response()
	user = request.validate_login(user_info)
	if request.method == "GET":
		todo_item_id = request.query().get("id", "")
		body = template("templates\\todo_edit.html").replace("{{item_id}}", todo_item_id)
		resp.body = body.encode("utf-8")
	else:
		form = request.form()
		todo_item_id = form.get("id", "")
		todo_item_title = form.get("title", "")
		todo = Todo.find_by(userid=user.id)[0]
		for t in todo.todos:
			if t.get("itemid") == int(todo_item_id):
				t["title"] = todo_item_title
		todo.del_by(userid=user.id)
		todo.save()
		resp.set_redirect("/todo")
	return resp

def routes_del(request):
	resp = Response()
	user = request.validate_login(user_info)
	if request.method == "GET":
		todo_item_id = request.query().get("id", "")
		todo = Todo.find_by(userid=user.id)[0]
		del_item = None
		for t in todo.todos:
			if t.get("itemid") == int(todo_item_id):
				del_item = t
		if del_item:
			todo.todos.remove(del_item)
		todo.del_by(userid=user.id)
		todo.save()
		resp.set_redirect("/todo")
	return resp



routes_todo_dict = {
	"/todo": routes_todo,
	"/todo/add": routes_add,
	"/todo/edit": routes_edit,
	"/todo/del": routes_del,
}