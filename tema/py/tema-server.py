#!/usr/bin/env python

from simpletext import SimpleText
import bluetooth
import os

def start(tableau):
  # tableau.display("Wait...")
  tableau.display_score("TEST_WHITE")
  # tableau.display_score("624*15464*40")
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

  tableau.display("Connected")

  try:
      msg = "";
      while True:
          data = client_sock.recv(1)          
          if not data:
              # FIXME doesn't work when sending empty string from Android
              break
          elif data == "\n":
              print("Received packet: {0}".format(msg))
              tableau.display_score(msg)
              msg = ""
          else:
              msg+=data
  except bluetooth.btcommon.BluetoothError as err:
      print("BT error: {0}".format(err))
      pass
  except OSError:
      pass
  print("Disconnected.")
  client_sock.close()
  server_sock.close()
  start(tableau)


simple_text = SimpleText()
simple_text.process()
start(simple_text)
