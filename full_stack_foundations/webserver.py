import cgi, cgitb
import requests
import re
from urllib.parse import parse_qs, parse_qsl, urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from run import session
from database_setup import Restaurant


class WebserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:

            regex = re.compile(r'/restaurant/[0-9]+/edit')
            if self.path.endswith('/restaurants'):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                output = ''
                for restaurant in restaurants:
                    output += '<h1> {restaurant} <br>'.format(restaurant=restaurant.name)
                    output += '<a href="/restaurant/{id}/edit">Edit</a> <br>'.format(id=restaurant.id)
                    output += '<a href="/restaurants">Delete</a> </h1> <br><br>'
                self.wfile.write(bytes(output, 'utf-8'))
                return

            elif self.path.endswith(regex.findall(self.path)[0]):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                print(self.path)
                output = ''
                output += "<form method='POST' enctype='multipart/form-data' action='/" \
                          "hello'><h2>Restaurant Name</h2><input name='edit_name'" \
                          "type='text'>"
                output += "<input type='submit' value='Submit'></form>"
                self.wfile.write(bytes(output, 'utf-8'))
                return

            elif self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ''
                output += '<html><body>Hello!'
                output += '<br><a href="/hola">Hola Page</a>'
                output += """<form method='POST' enctype='multipart/form-data' action='/hello'><h2> What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"""
                output += '</html></body>'
                self.wfile.write(bytes(output, 'utf-8'))
                print(bytes(output, 'utf-8'))
                return

            elif self.path.endswith('/hola'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ''
                output += '<html><body>Hola&#161'
                output += "<br><a href='/hello'>Hello Page</a>"
                output += "<form method='POST' enctype='multipart/form-data' action='/" \
                          "hello'><h2> What would you like me to say?</h2><input name='message'" \
                          " type='text'><input type='submit' value='Submit'></form>"
                output += '</body></html>'
                self.wfile.write(bytes(output, 'utf-8'))
                return

            elif self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                output = ''
                output += "<form method='POST' enctype='multipart/form-data' action='/" \
                          "hello'><h2>Restaurant Name</h2><input name='restaurant_name'" \
                          "type='text'>"
                output += "<input type='submit' value='Submit'></form>"
                self.wfile.write(bytes(output, 'utf-8'))
                return

        except IOError:
            self.send_error(404, 'File Not Found %s' % self.path)

    def do_POST(self):
        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
        if ctype == 'multipart/form-data':
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            fields = cgi.parse_multipart(self.rfile, pdict)
            messagecontent = fields.get('message',
                                        fields.get('restaurant_name', fields.get('edit_name')))[0].decode('utf-8')
            if fields.get('restaurant_name'):
                session.add(Restaurant(name=messagecontent))
                session.commit()
                print('New Restaurant Added!')
                output = '<a href="/restaurants"> <h1> GO TO RESTAURANTS PAGE </h1> </a>'
                self.wfile.write(bytes(output, 'utf-8'))
                return
            elif fields.get('edit_name'):
                url = urlparse(self.headers['Referer'])
                id_ = url.path.split('/')[2]
                print(id_)
                restaurant = session.query(Restaurant).get(id_)
                restaurant.name = messagecontent
                session.commit()
                print('Edited Restaurant!')
                output = '<a href="/restaurants"> <h1> GO TO RESTAURANTS PAGE </h1> </a>'
                self.wfile.write(bytes(output, 'utf-8'))
                return

        output = ''
        output += '<html><body>'
        output += '<h2> Okay, how about this: </h2>'
        output += '<h1> %s </h1>' % messagecontent
        output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
        output += '</html></body>'
        self.wfile.write(output.encode('utf-8'))


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebserverHandler)
        print('Web server running on port %s' % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print('^C entered, stopping web server...')
        server.socket.close()


if __name__ == '__main__':
    main()
