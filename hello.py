def wsgi_application(environ, start_response):
	start_response("200 OK", [("Content-Type", "text/plain")])
	return [environ['QUERY_STRING'].replace('&','\n')]
