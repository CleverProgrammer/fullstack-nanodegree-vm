import cgi
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from run import session
from database_setup import Restaurant


class WebserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ''
                output += '<html><body>Hello!'
                output += '<br><a href="/hola">Hola Page</a>'
                output += "<form method='POST' enctype='multipart/form-data' action='/" \
                          "hello'><h2> What would you like me to say?</h2><input name='message'" \
                          " type='text'><input type='submit' value='Submit'></form>"
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
                print(bytes(output, 'utf-8'))
                return

            elif self.path.endswith('/restaurants'):
                restaurants = session.query(Restaurant).all()
                output = ''
                for restaurant in restaurants:
                    output += '<h1> {restaurant} <br>'.format(restaurant=restaurant.name)
                    output += '<a href="/restaurants">Edit</a> <br>'
                    output += '<a href="/restaurants">Delete</a> </h1> <br><br>'
                self.wfile.write(bytes(output, 'utf-8'))
                return

        except IOError:
            self.send_error(404, 'File Not Found %s' % self.path)

    def do_POST(self):
        try:
            length = int(self.headers['Content-Length'])
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            post_data = parse_qs(self.rfile.read(length).decode('utf-8'))
            messagecontent = post_data.get(' name')[0].split('\n')[2]
            output = ''
            output += '<html><body>'
            output += '<h2> Okay, how about this: </h2>'
            output += '<h1> %s </h1>' % messagecontent
            output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
            output += '</html></body>'
            self.wfile.write(output.encode('utf-8'))
        except:
            pass


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
