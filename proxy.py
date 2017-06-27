from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import requests
import sqlite3 as lite

##Check for update.
try:
    if int(requests.get("https://raw.githubusercontent.com/wfscans/kanpani-tl-project/master/version").content) > 1:
        print "New version available! Check https://github.com/wfscans/kanpani-tl-project for more details."
except Exception as e:
    print "Failed to check for new version."
    
class Handler(BaseHTTPRequestHandler):
   
   def do_GET(self):
       self.send_response(200)
       self.send_header("Cache-Control","max-age=604800")
       self.end_headers()
       try:
            with open(self.path[self.path.index("/img/")+1:len(self.path)], 'rb') as f:
                self.wfile.write(f.read())
                return
       except Exception as e:
            pass

       headers = []
       for i in self.headers.headers:
        headers.append(i.split(":", 1)[0].strip())
        headers.append(i.split(":", 1)[1].strip())
       headers = iter(headers)
       headers = dict(zip(headers, headers))
       
       self.wfile.write(requests.get(self.path, headers=headers, stream=True).raw.data)
       
   
   def do_POST(self):
       self.send_response(200)
       self.end_headers()
       
       headers = []
       for i in self.headers.headers:
        headers.append(i.split(":", 1)[0].strip())
        headers.append(i.split(":", 1)[1].strip())
       headers = iter(headers)
       headers = dict(zip(headers, headers))
       rbody = self.rfile.read(int(self.headers.getheader('content-length'))) #Request body length
       
       
       res = requests.post(self.path, data=rbody, headers=headers, stream=True)
       
       if ("c=Quest.next" in self.path):            
            conn = lite.connect('kp_trans.db')
            cur = conn.cursor()
            res = res.raw.data
            conn.text_factory = str
            
            cur.execute("SELECT jp, eng, id FROM story WHERE map = ?", (rbody[len(rbody)-10:len(rbody)],))
            
            for row in cur:
                res = res.replace(row[0], row[1])
            
            self.wfile.write(res)
            
            conn.close()
       elif ("c=Quest.main_enter" in self.path) or ("c=Quest.special_enter" in self.path):
            conn = lite.connect('kp_trans.db')
            cur = conn.cursor()
            res = res.raw.data
            conn.text_factory = str
            
            
            cur.execute("SELECT jp, eng, id FROM story WHERE map = ?", (rbody[len(rbody)-29:len(rbody)-12],))

            for row in cur:
                res = res.replace(row[0], row[1])
            
            self.wfile.write(res)
            
            conn.close()
       elif ("c=Quest.main_stages" in self.path):
            conn = lite.connect('kp_trans.db')
            cur = conn.cursor()
            res = res.raw.data
            conn.text_factory = str
            
            cur.execute("SELECT jp, eng FROM desc WHERE map = ?", (rbody[-8:],))
                        
            for row in cur:
                res = res.replace(row[0], row[1])
                    
            self.wfile.write(res)
       else:
            self.wfile.write(res.raw.data)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    server = ThreadedHTTPServer(('localhost', 8899), Handler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()