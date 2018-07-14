#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from notepad import *
import mimetypes

# HTTPRequestHandler class
class Server(BaseHTTPRequestHandler):
    """ Simple CRUD server for notes """

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        print (str(length))

        query = self.rfile.read(length).decode('utf-8')
        post_data = parse_qs(query)

        man = Manager()
        if post_data.get("title") and post_data.get("text"):
            title = post_data["title"][0]
            text  = post_data["text"][0]

            man.add_note(Note(title, text))
            man.save_with_pickle()

        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def do_query(self, query):
        query_dict  = dict(qc.split("=") for qc in query.split("&"))
        if query_dict.get("action"):
            action = query_dict["action"]
            if query_dict.get("num"):
                try:
                    num = int(query_dict["num"])
                except:
                    self.send_response(400)
                    return None

            if action == "del":
                man = Manager()
                man.del_note(num)
                man.save_with_pickle()
                gen = Generator(man.notes)

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                message = gen.get_html().encode("utf-8")
                self.wfile.write(message)

    def do_file(self, path):
        """" Not secure at all, use only for personal purpose """

        try:
            filepath = path.path
            file = open("." + filepath)
        except IOError:
            #self.send_response(404)
            self.send_error(404, "File not found")

            self.send_header("Content-type", "text/html")
            self.end_headers()
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

        return None

def run_server():
    print('starting server...')

    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('', 8081)
    httpd = HTTPServer(server_address, Server)
    print('running server...')
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
