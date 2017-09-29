#!/usr/bin/env python2.7
import RPi.GPIO as GPIO
import pika
import time

bouncetime=300

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#GPIO.setup(17, GPIO.IN)
#GPIO.setup(27, GPIO.IN)
#GPIO.setup(22, GPIO.IN)

def send_message(message):
  connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
  channel = connection.channel()
  channel.basic_publish(exchange='', routing_key='buzzer', body=message)
  connection.close()


def button1(channel):
  count_j0+=1
  print("Button 1 pressed", count_j0)
  send_message("button1\n")

def button2(channel):
  count_j0+=1
  print ("Button 2 Pressed", count_j1)
  send_message("button2\n")

def button3(channel):
  count_j0+=1
  print ("Button 3 Pressed", count_j2)
  send_message("button3\n")

GPIO.add_event_detect(17, GPIO.FALLING, callback=button1, bouncetime=300)
GPIO.add_event_detect(27, GPIO.FALLING, callback=button2, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=button3, bouncetime=400)

#GPIO.add_event_detect(17, GPIO.FALLING, callback=button1)
#GPIO.add_event_detect(27, GPIO.FALLING, callback=button2)
#GPIO.add_event_detect(22, GPIO.FALLING, callback=button3)

count_j0=0
count_j1=0
count_j2=0

try:
  time.sleep(1000)

except KeyboardInterrupt:
  GPIO.cleanup() # clean up GPIO on CTRL+C exit
GPIO.cleanup()   # clean up GPIO on normal exit
