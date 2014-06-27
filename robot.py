#!/usr/bin/python

# python server to pass http requests to the serial port

# yuri - Jun 2014

# adapted from http://matt.might.net/articles/ios-multitouch-robot-control/

# requires a web page/app to send GET requests

# TODO: properly implement "spin" for rotation

import time
from os import curdir, sep
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from urlparse import urlparse, parse_qs
import serial

HOST_NAME = 'tusker.local' # change to local host name
PORT_NUMBER = 8080         # 80 will conflict with lighttpd/apache

robot = serial.Serial('/dev/ttyACM0', 9600)

def handle_move(query):
  print "speedL(%s)" % float(query['speedL'][0])
  print "speedR(%s)" % float(query['speedR'][0])
  robot.write("speedL:%s\r\n" % float(query['speedL'][0]))
  robot.write("speedR:%s\r\n" % float(query['speedR'][0]))

def handle_spin(query):
  print "speedL(%s)" % float(query['speedL'][0])
  print "speedR(%s)" % float(query['speedR'][0])
  robot.write("speedL:%s\r\n" % float(query['speedL'][0]))
  robot.write("speedR:%s\r\n" % float(query['speedR'][0]))

def handle_stop(query):
  print "Stop"
  robot.write("speedL:0.0\r\n")
  robot.write("speedR:0.0\r\n")


class ServerHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path == "/":
      self.path = "/index.html"

    url = urlparse(self.path)
    action = url.path[1:]
    query = parse_qs(url.query)
    print "action: ", action
    print "query:  ", query

    if action == "move":
      handle_move(query)
    elif action == "spin":
      handle_spin(query)
    elif action == "stop":
      handle_stop(query) 
    else: # grab a file
      try:
        print "sending file: ", url.path
        f = open(curdir + sep + url.path) 
        self.send_response(200)
        if url.path.endswith('.html'):
          self.send_header('Content-type', 'text/html')
        elif url.path.endswith('.js'):
          self.send_header('Content-type', 'text/javascript')
        elif url.path.endswith('.gif'):
          self.send_header('Content-type', 'image/gif')
        self.end_headers()
        self.wfile.write(f.read()); f.close()
        return
      except IOError:
        self.send_error(404,'File Not Found: %s' % self.path)
        return
 
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    self.wfile.write('OK: ' + self.path)

if __name__ == '__main__':
  httpd = HTTPServer((HOST_NAME, PORT_NUMBER), ServerHandler)
  print time.asctime(), "Server started - %s:%s" % (HOST_NAME, PORT_NUMBER)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
  httpd.server_close()
  print time.asctime(), "Server stopped - %s:%s" % (HOST_NAME, PORT_NUMBER)
