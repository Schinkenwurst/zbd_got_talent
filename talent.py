#!/usr/bin/python3

from tkinter import *
import pika
from threading import Thread
import simpleaudio as sa




#######################################################################
# Consumer for RabbitMQ
#######################################################################
def amqp_consume():
  # Callback on message
  def onmessage(ch, method, properties, body):
    body = body.decode('utf8')
    print("message: ", body)

    if body == "joury0":
      print("COMMAND: alert jury0")
      set_alert("joury0")
      play_alarm()

    elif body == "joury1":
      print("COMMAND: alert jury0")
      set_alert("joury1")
      play_alarm()

    elif body == "joury2":
      print("COMMAND: alert jury0")
      set_alert("joury2")
      play_alarm()

    elif body == "reset":
      print("COMMAND: reset")
      reset_alert()

    else:
      print("COMMAND: UNKNOWN")

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
# Consumer for RabbitMQ
#######################################################################
def play_alarm():
  print("DEBUG: Plaing alarm")
  wave_obj = sa.WaveObject.from_wave_file("buzzer1.wav")
  play_obj = wave_obj.play()
#  play_obj.wait_done()


#######################################################################
# Hide and set alerts
#######################################################################
def set_alert(action):
  if action == "joury0":
    pic_j0 = Label( root, bg="black", image=p_alert )
    lbl_j0 = Label( root, bg="black", fg="grey", text="Eva", font=("Helvetica", 24))

    pic_j0.grid( row=0, column=1, padx='5', pady='5', sticky='ew' )
    lbl_j0.grid( row=0, column=0, padx='5', pady='5', sticky='ew' )

  elif action == "joury1":
    pic_j1 = Label( root, bg="black", image=p_alert )
    lbl_j1 = Label( root, bg="black", fg="grey", text="Fabian", font=("Helvetica", 24))

    pic_j1.grid( row=0, column=3, padx='5', pady='5', sticky='ew' )
    lbl_j1.grid( row=0, column=2, padx='5', pady='5', sticky='ew' )

  elif action == "joury2":
    pic_j2 = Label( root, bg="black", image=p_alert )
    lbl_j2 = Label( root, bg="black", fg="grey", text="Tim", font=("Helvetica", 24))

    pic_j2.grid( row=0, column=5, padx='5', pady='5', sticky='ew' )
    lbl_j2.grid( row=0, column=4, padx='5', pady='5', sticky='ew' )
  
  # Play alarm sound ;)
  play_alarm()

def reset_alert():
    pic_j0 = Label( root, bg="black", image=p_blank )
    pic_j1 = Label( root, bg="black", image=p_blank )
    pic_j2 = Label( root, bg="black", image=p_blank )
    lbl_j0 = Label( root, bg="black", fg="grey", text="", font=("Helvetica", 24))
    lbl_j1 = Label( root, bg="black", fg="grey", text="", font=("Helvetica", 24))
    lbl_j2 = Label( root, bg="black", fg="grey", text="", font=("Helvetica", 24))

    pic_j0.grid( row=0, column=1, padx='5', pady='5', sticky='ew' )
    pic_j1.grid( row=0, column=3, padx='5', pady='5', sticky='ew' )
    pic_j2.grid( row=0, column=5, padx='5', pady='5', sticky='ew' )
    lbl_j0.grid( row=0, column=0, padx='5', pady='5', sticky='ew' )
    lbl_j1.grid( row=0, column=2, padx='5', pady='5', sticky='ew' )
    lbl_j2.grid( row=0, column=4, padx='5', pady='5', sticky='ew' )


#######################################################################
# Button actions 
#######################################################################

def btn_set_alert_j0():
  set_alert("joury0")
def btn_set_alert_j1():
  set_alert("joury1")
def btn_set_alert_j2():
  set_alert("joury2")
def btn_reset_alert():
  reset_alert()


#######################################################################
# Main 
#######################################################################

###################################
# Configuration parameter
stand_alone="true"

###################################
# Create main GUI object
root = Tk()
root.configure(background='black')
root.title("ZBD got Talent")

# Configure Layout
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)
root.columnconfigure(5, weight=1)
###################################
# Load pictures
p_alert = PhotoImage(file="alert.png")
p_blank = PhotoImage(file="blank.png")

###################################
# Set alert buttons
if stand_alone == "false":
  # Start consumer for RabbitMQ
  t1 = Thread( target=amqp_consume )
  t1.saemon = True
  t1.start()
else:
  # alert buttons for testing
  b_j0_set = Button( root, text="Set Alert", command=btn_set_alert_j0 )
  b_j1_set = Button( root, text="Set Alert", command=btn_set_alert_j1 )
  b_j2_set = Button( root, text="Set Alert", command=btn_set_alert_j2 )
  b_j0_set.grid( row=2, column=1 )
  b_j1_set.grid( row=2, column=3 )
  b_j2_set.grid( row=2, column=5 )
  
  # hide alert button for testing
  b_hide = Button( root, text="Clear Alert", command=btn_reset_alert )
  b_hide.grid( column=3, row=3 )
  
  # Testlabel
  #ltest = Label( root, text="wurst" )
  #ltest.grid( column=1, row=3 )

# Start main GUI
try:
  root.mainloop()
except KeyboardInterrupt:
  exit
