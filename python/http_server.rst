=============================
http.server
=============================



::

    import http.server
    import socketserver

    class MyHandler (http.server.SimpleHTTPRequestHandler):

        def do_POST():
            pass

    PORT = 8080

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()



::

    python3 myserver.py
