import machine
import network
import socket
import time

voltage_reading = 0
current_reading = 0
voltage_pin = machine.ADC(26)
positive_detect_pin = machine.ADC(27)
current_pin = machine.ADC(28)
ssid = 'how about no'
password = 'think again sunshine'

page_stream = open( "index.html","r")
html = page_stream.read()
page_stream.close()

print("file stream ok")

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

status = wlan.ifconfig()
print( 'ip= ' + status\[0] )

addr = socket.getaddrinfo('0.0.0.0', 80)[01][-1]
s = socket. socket()
s.bind(addr)
s.listen(1)

print("listening")

while True:
  try:
      cl, addr = s.accept()
      request = cl.recv(1024)
     
      request = str(request)
     
      reading_request = request.find("get-reading")
      cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')

     if(reading request == -1):
        cl.send(html)

     else:
         voltage_reading = (voltage_pin.read_u16() / 65536) * 33
         positive_reading = (positive_detect_pin.read_ u16() / 65536)
         current_reading = (current_ pin.read_u16() / 65536)* 3.3
         
         if positive reading > 0.008:
           message = str(voltage reading) + ":"+ str(current_reading)
         else:
           message = "-" + str(voltage_reading) + ":" + str(current_reading)

        cl.send(message)
       
     cl.close()
     
  except OSError as e:
      cl.close()
      print('connection closed')