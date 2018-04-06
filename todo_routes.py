from objects import Response
from routes import template
from routes import cookie_info
from models import Todo
from routes import login_required
from routes import redirect
from utils import log


@login_required
def routes_todo(request):
	resp = Response()
	body = template("templates\\todo_index.html")
	sess = request.session(cookie_info)
	userid = sess.get("userid")
	lst = Todo.find_by(userid=userid)
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
	return resp

@login_required
def routes_add(request):
	if request.method == "POST":
		userid = request.session(cookie_info).get("userid")
		lst = Todo.find_by(userid=userid)

		form = request.form()
		title = form.get("title")
		if lst == []:
			todo = Todo.new({
				"userid": userid,
			})
		else:
			todo = lst[0]

		i = len(todo.todos)
		todo_item = {
			"itemid": i + 1,
			"title": title,
		}
		todo.todos.append(todo_item)
		todo.del_by(userid=userid)
		todo.save()
		return redirect("/todo")
	else:
		return redirect("/index")

@login_required
def routes_edit(request):
	resp = Response()
	userid = request.session(cookie_info).get("userid")
	if request.method == "GET":
		todo_item_id = request.query().get("id", "")
		body = template("templates\\todo_edit.html").replace("{{item_id}}", todo_item_id)
		resp.body = body.encode("utf-8")
		return resp
	else:
		form = request.form()
		todo_item_id = form.get("id", "")
		todo_item_title = form.get("title", "")
		todo = Todo.find_by(userid=userid)[0]
		for t in todo.todos:
			if t.get("itemid") == int(todo_item_id):
				t["title"] = todo_item_title
		todo.del_by(userid=userid)
		todo.save()
		return redirect("/todo")



@login_required
def routes_del(request):
	userid = request.session(cookie_info).get("userid")
	if request.method == "GET":
		todo_item_id = request.query().get("id", "")
		todo = Todo.find_by(userid=userid)[0]
		del_item = None
		for t in todo.todos:
			if t.get("itemid") == int(todo_item_id):
				del_item = t
		if del_item:
			todo.todos.remove(del_item)
		todo.del_by(userid=userid)
		todo.save()
		return redirect("/todo")
	else:
		return redirect("/index")



routes_todo_dict = {
	"/todo": routes_todo,
	"/todo/add": routes_add,
	"/todo/edit": routes_edit,
	"/todo/del": routes_del,
}