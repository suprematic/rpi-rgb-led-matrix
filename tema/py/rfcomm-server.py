#!/usr/bin/env python3

import bluetooth
import os
 
def start():
  server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
  server_sock.bind(("", bluetooth.PORT_ANY))
  server_sock.listen(1)

  port = server_sock.getsockname()[1]

  uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

  bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                              service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                              profiles=[bluetooth.SERIAL_PORT_PROFILE],
                              # protocols=[bluetooth.OBEX_UUID]
                              )
  print("Waiting for connection on RFCOMM channel {0}".format(port))
  client_sock, client_info = server_sock.accept()
  print("Accepted connection from {0}".format(client_info))

  try:
      while True:
          data = client_sock.recv(1024)
          if not data:
              break
          print("Received", data)
          os.system('python runtext.py -t ' + data)
  except bluetooth.btcommon.BluetoothError as err:
      print("BT error: {0}".format(err))
      pass
  except OSError:
      pass
  print("Disconnected.")
  client_sock.close()
  server_sock.close()
  start()


start()
