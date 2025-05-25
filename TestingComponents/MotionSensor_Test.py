import RPi.GPIO as GPIO
import time

output_pin = 27
input_pin = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(input_pin, GPIO.IN)
GPIO.setup(output_pin,GPIO.OUT)

def main():
    while True:
        in_status = GPIO.input(input_pin)
        while not(in_status):
           print("No motion sensed.")
           time.sleep(2)
           in_status = GPIO.input(input_pin)
        while (in_status):
           print("Motion sensed!")
           time.sleep(2)
           in_status = GPIO.input(input_pin)
            
if __name__ == "__main":
    main()

