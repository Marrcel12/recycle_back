from http.server import HTTPServer, BaseHTTPRequestHandler
import json
# obrabianie url
def url_to_list(url):
    url_to_process=url[int(str(url)[1:].find("/"))+2:]
    flag=0
    list={}
    key=""
    value=""
    for i in url_to_process:
            if i =="=" or i == "%":
                    if i == "=":
                        list[key]=""
                        flag=1
                    if i== "%":
                        list[key]=value
                        key=""
                        value=""
                        flag=0
            else:
                    if flag ==0:
                        key+=i
                    if flag ==1:
                        value+=i
    return(list)
class Serv(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        url=self.path
        # scan
        if  'scan' in url:
            requests=url_to_list(url) 
            print(requests)         
            #  database

            materials=['dummy','dumm2']
            bins=['dummy','dumm2']
            name="lama"

            self._set_headers()
            # send
            self.wfile.write(json.dumps({'hello': 'Test1' }).encode("utf-8"))


        #upcyling
        if  'upcyling' in url:
            
            requests=url_to_list(url) 
            print(requests)
            # database
            tags=""
            number_of_requests=0
            photo_url=""
            name=""
            #json
            self._set_headers()
            self.wfile.write(json.dumps({'hello': 'Test1' }).encode("utf-8"))

        # facts
        if  'facts' in url:
            requests=url_to_list(url) 
            print(requests)
            # database
            print('facts')
            #json_send
            self._set_headers()
            self.wfile.write(json.dumps({'hello': 'Test1' }).encode("utf-8"))


        # goals
        if  'goals' in url:
            requests=url_to_list(url) 
            print('goals')
             #json_send
            self._set_headers()
            self.wfile.write(json.dumps({'hello': 'Test1' }).encode("utf-8"))

        # user
        if  'user' in url:
            requests=url_to_list(url) 
            print('user')
             #json_send
            self._set_headers()
            self.wfile.write(json.dumps({'hello': 'Test1' }).encode("utf-8"))


httpd = HTTPServer(('localhost', 8080), Serv)
httpd.serve_forever()