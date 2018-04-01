from SimpleClient import parsed_url

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

def main():
	s = ""
	p = s.split("e")
	print(p)

if __name__ == "__main__":
	main()