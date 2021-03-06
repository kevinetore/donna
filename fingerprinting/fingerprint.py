import warnings
import json
import RPi.GPIO as GPIO
import time as time
import threading
from threading import Thread
warnings.filterwarnings("ignore")

from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer

GPIO.setmode(GPIO.BOARD)
pins = [3,5,8,15,16] # In correct order of GPIO on Raspberry Pi
second_pins = [7,11,13,10,12]

board_pins = zip(pins, second_pins)
reversed_board_pins = board_pins[::-1]

GPIO.setup(pins+second_pins, GPIO.OUT)

# load db info from a JSON file
with open("/home/pi/projects/fingerprinting/database.cnf") as f:
    config = json.load(f)   

def piBoard():
    recognizing = 0
    while (recognizing < 20):
        for pin in board_pins:
            GPIO.output(
                pin[0], GPIO.HIGH
            )
            GPIO.output(
                pin[1], GPIO.HIGH
            )
            time.sleep(0.1)
            GPIO.output(
                pin[0], GPIO.LOW
            )
            GPIO.output(
                pin[1], GPIO.LOW
            )
        for pin in reversed_board_pins:
            GPIO.output(
                pin[0], GPIO.HIGH
            )
            GPIO.output(
                pin[1], GPIO.HIGH
            )
            time.sleep(0.1)
            GPIO.output(
                pin[0], GPIO.LOW
            )
            GPIO.output(
                pin[1], GPIO.LOW
            )
        recognizing += 1
    # GPIO.cleanup()
        
def recognizeSong():
    # Have to run multiple threads at the same time in order to let the 5mm LED's blink and recognize the music
    Thread(target = piBoard).start()
    # create a Dejavu instance
    djv = Dejavu(config)

    # Fingerprint mp3's in mp3 directory
    djv.fingerprint_directory("mp3", [".mp3"])
    secs = 10
    
    # I'm trying to catch the exception because sometimes Alsa throws a weird -9981 input overflowed error
    # Still this is a very very bad implementation. First it would take ages and after the 100th time Donna would just crash
    for i in range(0,100):
        while True:
            try:
                return djv.recognize(MicrophoneRecognizer, seconds=secs)
            except IOError:
                continue
            break
