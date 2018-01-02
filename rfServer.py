import os
import json
import requests
import time
import broadlink
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

PATH_TO_CODES = "/home/pi/rmminiserver/rfcodes/"

rfCodes = {}

rfCodesList = os.listdir(PATH_TO_CODES)
for rfCodeName in rfCodesList:
    with open(PATH_TO_CODES+rfCodeName, 'r') as f:
        rfCodes[rfCodeName] = f.read()

type = int("0x2712", 0)
host = "192.168.1.18"
mac_raw = "34EA34439EC9"
mac = bytearray.fromhex(mac_raw)

device = broadlink.gendevice(type, (host, 80), mac)
device.auth()

PORT_NUMBER = 8074 

def basicSend(command):
    data = bytearray.fromhex(''.join(rfCodes[command]))
    device.send_data(data)
    return {'SUCCESS':'TRUE'}


def setInput(targetInput):
  resp = {"ERROR": "INVALID TARGET INPUT"}
  numPress = ""

  if targetInput == "n64":
      numPress = "tv_1"
  elif targetInput == "roku":
      numPress = "tv_3"
  elif targetInput == "xbox":
      numPress = "tv_4"
  elif targetInput == "shield":
      numPress = "tv_5"

  if numPress != "":
      basicSend("tv_input")
      time.sleep(0.25)
      basicSend(numPress)
      resp = {"SUCCESS":"TRUE"}

  return resp


def setBrightness(targetBrightness):

  resp = {"ERROR": "BRIGHTNESS NOT IN RANGE"}
  numPress = ""
  
  try:
      if int(targetBrightness) >= 1 and int(targetBrightness) <= 5:
          numPress = "tv_"+str(targetBrightness)
  except ValueError:
      resp = {"ERROR": "INVALID BRIGHTNESS VALUE"}

  if numPress != "":
      basicSend("tv_picmode")
      time.sleep(0.25)
      basicSend(numPress)
      resp = {"SUCCESS":"TRUE"}
  return resp



class myHandler(BaseHTTPRequestHandler):

    def setup(self):
        BaseHTTPRequestHandler.setup(self)
        self.request.settimeout(60)

    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-type','application/javascript')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        rPath = self.path.split('/')
        try:
            if rPath[1] == "tv_setinput":
                resp = setInput(rPath[2])
            elif rPath[1] == "tv_setbrightness":
                resp = setBrightness(rPath[2])
            elif rPath[1] == "tv_toggle":
                resp = basicSend('tv_power')
            elif rPath[1] == "tv_mute":
                resp = basicSend('tv_mute')
            elif rPath[1] == "candles_on":
                resp = basicSend('candles_on')
            elif rPath[1] == "candles_off":
                resp = basicSend('candles_off')
            else:
                resp = {'ERROR': 'UNKNOWN ENDPOINT'}
        except IndexError:
            resp = {'ERROR': 'INVALID REQUEST'}
            
        self.wfile.write(json.dumps(resp))
        return

try:
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER
    server.serve_forever()
except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()


def tvMute():
    data = bytearray.fromhex(''.join(rfCodes['tv_mute']))
    device.send_data(data)
