#!/usr/bin/python3

from tkinter import *
import pika
from threading import Thread
import simpleaudio as sa

#######################################################################
# Consumer for RabbitMQ
def amqp_consume():
  # Callback on message
  def onmessage(ch, method, properties, body):
    body = body.decode('utf8')

    if body == "jury0":
      print("[INFO] Alert jury0")
      set_alert("jury0")

    elif body == "jury1":
      print("[INFO] Alert jury1")
      set_alert("jury1")

    elif body == "jury2":
      print("[INFO] Alert jury2")
      set_alert("jury2")

    elif body == "reset":
      print("[INFO] Reset")
      reset_alert()

    else:
      print("[INFO] UNKNOWN")

    # Newline for nicer looking
    print()

  # Main of amqp_consume
  amqp_credentials = pika.PlainCredentials('buzzer', 'buzzer')
  amqp_parameter = pika.ConnectionParameters('192.168.0.127', 5672, '/', amqp_credentials)
  amqp_connection = pika.BlockingConnection(amqp_parameter)
  amqp_channel = amqp_connection.channel()

  amqp_channel.queue_declare(queue='buzzer', auto_delete=True)
  amqp_channel.basic_consume(onmessage, queue='buzzer', no_ack=True)

  try:
    amqp_channel.start_consuming()
  except KeyboardInterrupt:
    amqp_channel.stop_consuming()
    amqp_connection.close()


#######################################################################
# Play buzzer-sound
def play_alarm():
  print("[INFO] Playing sound")
  wave_obj = sa.WaveObject.from_wave_file("sounds/buzzer1.wav")
  play_obj = wave_obj.play()
  play_obj.wait_done()


#######################################################################
# Set alerts and call buzzer-sound routine
def set_alert(action):
  if action == "jury0":
    pic_j0 = Label( root, bg="black", image=pic_alert_j0 )
    pic_j0.grid( row=0, column=0, padx='0', pady='0' )
    play_alarm() # call buzzer-sound routine

  elif action == "jury1":
    pic_j1 = Label( root, bg="black", image=pic_alert_j1 )
    pic_j1.grid( row=0, column=1, padx='0', pady='0' )
    play_alarm() # call buzzer-sound routine

  elif action == "jury2":
    pic_j2 = Label( root, bg="black", image=pic_alert_j2 )
    pic_j2.grid( row=0, column=2, padx='0', pady='0' )
    play_alarm() # call buzzer-sound routine


#######################################################################
# Reset alerts
def reset_alert():
    pic_j0 = Label( root, bg="black", image=pic_blank_j0 )
    pic_j1 = Label( root, bg="black", image=pic_blank_j1 )
    pic_j2 = Label( root, bg="black", image=pic_blank_j2 )

    pic_j0.grid( row=0, column=0, padx='5', pady='5' )
    pic_j1.grid( row=0, column=1, padx='5', pady='5' )
    pic_j2.grid( row=0, column=2, padx='5', pady='5' )


#######################################################################
# Button actions
def btn_set_alert_j0():
  set_alert("jury0")
def btn_set_alert_j1():
  set_alert("jury1")
def btn_set_alert_j2():
  set_alert("jury2")
def btn_reset_alert():
  reset_alert()


#######################################################################
# Main
#######################################################################

###################################
# Configuration parameter
stand_alone="false"

###################################
# Create main GUI object
root = Tk()
root.configure(background='black')
root.title("ZBD got Talent")

# Configure Layout
root.columnconfigure(0, weight=5)
root.columnconfigure(1, weight=0)
root.columnconfigure(2, weight=5)

###################################
# Load pictures
pic_alert_j0 = PhotoImage(file="images/alert_bruce.png")
pic_alert_j1 = PhotoImage(file="images/alert_nazan.png")
pic_alert_j2 = PhotoImage(file="images/alert_dieter.png")
pic_blank_j0 = PhotoImage(file="images/blank_bruce.png")
pic_blank_j1 = PhotoImage(file="images/blank_nazan.png")
pic_blank_j2 = PhotoImage(file="images/blank_dieter.png")

###################################
# Init
reset_alert()

###################################
# Start RabbitMQ-Consumer or use buttons for simulation
if stand_alone == "false":
  t1 = Thread( target=amqp_consume )
#  t1.saemon = True
  t1.start()
else:
  b_j0_set = Button( root, text="Set Alert", command=btn_set_alert_j0 )
  b_j1_set = Button( root, text="Set Alert", command=btn_set_alert_j1 )
  b_j2_set = Button( root, text="Set Alert", command=btn_set_alert_j2 )
  b_j0_set.grid( row=1, column=0 )
  b_j1_set.grid( row=1, column=1 )
  b_j2_set.grid( row=1, column=2 )

  # hide alert button for testing
  b_hide = Button( root, text="Clear Alert", command=btn_reset_alert )
  b_hide.grid( row=2, column=1 )

# Start main GUI
try:
  root.mainloop()
except KeyboardInterrupt:
  exit
