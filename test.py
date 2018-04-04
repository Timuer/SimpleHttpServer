from SimpleClient import parsed_url
from models import User
from SimpleServer import Response
from utils import log




def test_parsed_url():
	test_items = [
		("http://localhost:80/index", ("http", "localhost", 80, "/index")),
		("https://www.douban.com/top250", ("https", "www.douban.com", 443, "/top250")),
		("https://g.cn/path1/path2?a=aaa", ("https", "g.cn", 443, "/path1/path2")),
		("https://g.cn/", ("https", "g.cn", 443, "/")),
	]
	i = 0
	for item in test_items:
		i += 1
		url_info = parsed_url(item[0])
		item = item[1]
		error = "test item {}: {} parse error '{}' != '{}'"
		assert url_info["protocol"] == item[0], error.format(i, "protocol", url_info["protocol"], item[0])
		assert url_info["host"] == item[1], error.format(i, "host", url_info["host"], item[1])
		assert url_info["port"] == item[2], error.format(i, "port", url_info["port"], item[2])
		assert url_info["path"] == item[3], error.format(i, "path", url_info["path"], item[3])


def test_models_save():
	a = {
		"username": "tianmu",
		"password": "12345",
	}
	u1 = User.new(a)
	u1.save()
	b = {
		"username": "hhhh",
		"password": "234",
	}
	u2 = User.new(b)
	u2.save()
	c = {
		"username": "aaa",
		"password": "fsdf",
	}
	u3 = User.new(c)
	u3.save()


def test_models_find_by():
	u = User.find_by(username="tianmu")
	if u:
		log(u)
	else:
		log("no model find")


def test_models_all():
	users = User.all()
	log([u for u in users])


def test_response():
	resp = Response()
	resp.add_header("Set-Cookie", "name=tianmu")
	log(resp.data())


def main():
	test_response()


if __name__ == "__main__":
	main()