import json
from utils import log
import uuid
import time


class Model(object):
	@classmethod
	def getid(cls):
		return str(uuid.uuid1())

	@classmethod
	def model_path(cls):
		name = cls.__name__
		path = "db\\{}.json".format(name)
		return path

	@classmethod
	def new(cls, form):
		model = cls(form)
		return model

	@classmethod
	def all(cls):
		path = cls.model_path()
		with open(path, encoding="utf-8") as f:
			s = f.read()
			if s:
				models = json.loads(s)
				return [cls.new(m) for m in models if m != None]
			else:
				return []

	@classmethod
	def find_by(cls, **kwargs):
		models = cls.all()
		if models:
			return [m for m in models if cls.match(m, kwargs)]
		else:
			return []

	@classmethod
	def match(cls, model, kwargs):
		flag = True
		for k, v in kwargs.items():
			if model.__dict__.get(k) != v:
				flag = False
		return flag

	def save(self):
		path = self.model_path()
		models = self.all()
		self.id = self.getid()
		models.append(self)
		model_list = [m.__dict__ for m in models]
		with open(path, "w+", encoding="utf-8") as f:
			s = json.dumps(model_list, indent=2, ensure_ascii=False)
			f.write(s)

	def del_by(self, **kwargs):
		models = self.all()
		del_item = None
		for m in models:
			if self.match(m, kwargs):
				del_item = m
		if del_item:
			path = self.model_path()
			models.remove(del_item)
			model_list = [m.__dict__ for m in models]
			with open(path, "w+", encoding="utf-8") as f:
				s = json.dumps(model_list, indent=2, ensure_ascii=False)
				f.write(s)

	def __repr__(self):
		classname = self.__class__.__name__
		properties = ["{}: ({})".format(k, v) for k, v in self.__dict__.items()]
		s = "\n".join(properties)
		return "< {}\n{} >\n".format(classname, s)


class User(Model):
	def __init__(self, form):
		self.id = form.get("id", None)
		self.username = form.get("username", "")
		self.password = form.get("password", "")
		self.description = form.get("description", "")

	def validate_login(self):
		users = self.all()
		for u in users:
			if u.username == self.username and u.password == self.password:
				return u
		return None

	def validate_register(self):
		if len(self.username) < 2 or len(self.password) < 2:
			return False
		users = self.all()
		for u in users:
			if u.username == self.username:
				return False
		return True


class Todo(Model):
	def __init__(self, form):
		self.id = form.get("id", None)
		self.todos = form.get("todos", [])
		self.userid = form.get("userid", None)

