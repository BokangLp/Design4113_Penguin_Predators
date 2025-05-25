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
            GPIO.output(output_pin, GPIO.HIGH)
            in_status = GPIO.input(input_pin)
        while (in_status):
            GPIO.output(output_pin, GPIO.HIGH)
            time.sleep(0.0025)
            GPIO.output(output_pin, GPIO.LOW)
            time.sleep(0.0025)
            in_status = GPIO.input(input_pin)
            


if __name__ == "__main":
    main()