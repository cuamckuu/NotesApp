#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from notepad import *
import mimetypes

# HTTPRequestHandler class
class Server(BaseHTTPRequestHandler):
    """ Simple CRUD server for notes """

#    def parse_POST(self):
#        ctype, pdict = parse_header(self.headers['content-type'])
#        if ctype == 'multipart/form-data':
#            postvars = parse_multipart(self.rfile, pdict)
#        elif ctype == 'application/x-www-form-urlencoded':
#            length = int(self.headers['content-length'])
#            postvars = parse_qs(
#                    self.rfile.read(length),
#                    keep_blank_values=1)
#        else:
#            postvars = {}
#        return postvars
#
#    def do_POST(self):
#        """ POST request for Create notes """
#        # postvars = self.parse_POST()
#        pass

    def do_query(self, query):
        self.send_response(200)

        self.send_header("Content-type", "text/html")
        self.end_headers()

        query_components = dict(qc.split("=") for qc in query.split("&"))
        print(query_components)

        man = Manager()
        gen = Generator(man.notes)

        message = gen.get_html().encode("utf-8")
        self.wfile.write(message)

    def do_file(self, path):
        """" Not secure at all, use only for personal purpose """

        try:
            filepath = path.path
            file = open("." + filepath)
        except IOError:
            self.send_error(404, "File not found")
        else:
            self.send_response(200)
            mimetype, _ = mimetypes.guess_type(filepath)

            self.send_header("Content-type", mimetype)
            self.end_headers()

            for line in file:
                self.wfile.write(bytes(line, "utf-8"))

    def do_index(self):
        self.send_response(200)

        self.send_header("Content-type", "text/html")
        self.end_headers()

        man = Manager()
        gen = Generator(man.notes)

        message = gen.get_html()
        self.wfile.write(bytes(message, "utf-8"))

    def do_GET(self):
        """ GET requersts for Read notes """
        path = urlparse(self.path)
        query = path.query
        allowed_filetypes = (".html", ".css", ".png",
                             ".jpg",  ".gif", ".ico",
                             ".js")

        if query:
            self.do_query(query)
        elif path.path.endswith(allowed_filetypes):
            self.do_file(path)
        else:
            self.do_index()


def run_server():
    print('starting server...')

    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('', 8081)
    httpd = HTTPServer(server_address, Server)
    print('running server...')
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
