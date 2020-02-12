from http.server import HTTPServer, BaseHTTPRequestHandler
import json
class Serv(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        url=self.path
        # scan
        if  'scan' in url:
            # search 
            code= url.split("/")[2]
           
            # request do bazy

            materials=['dummy','dumm2']
            bins=['dummy','dumm2']
            name="lama"

            self._set_headers()
            # send
            self.wfile.write(json.dumps({'hello': code , 'materials': materials}).encode("utf-8"))


        #upcyling
        if  'upcyling' in url:
            print('upcyling')

        # facts
        if  'facts' in url:
            print('facts')

        # goals
        if  'goals' in url:
            print('goals')

        # user
        if  'user' in url:
            print('user')


httpd = HTTPServer(('localhost', 8080), Serv)
httpd.serve_forever()