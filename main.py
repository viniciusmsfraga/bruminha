import pygame
import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
 
GPIO_TRIGGER_TOP = 27
GPIO_ECHO_TOP = 17
GPIO_ECHO_MIDDLE = 22
GPIO_TRIGGER_MIDDLE = 23
GPIO_ECHO_BOTTOM = 5
GPIO_TRIGGER_BOTTOM = 6 
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER_TOP, GPIO.OUT)
GPIO.setup(GPIO_ECHO_TOP, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_MIDDLE, GPIO.OUT)
GPIO.setup(GPIO_ECHO_MIDDLE, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_BOTTOM, GPIO.OUT)
GPIO.setup(GPIO_ECHO_BOTTOM, GPIO.IN)

def check_ultrasonic(sensor, test):
    while GPIO.input(sensor) == test:
        pass
    return time.time()


def sensor_distance(sensor):
    StartTime = check_ultrasonic(sensor,0)
    StopTime = check_ultrasonic(sensor, 1)
    
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    return (TimeElapsed * 34300) / 2


def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER_TOP, True)
    GPIO.output(GPIO_TRIGGER_MIDDLE, True)
    GPIO.output(GPIO_TRIGGER_BOTTOM, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_TOP, False)
    GPIO.output(GPIO_TRIGGER_MIDDLE, False)
    GPIO.output(GPIO_TRIGGER_BOTTOM, False)
    
    top_distance = sensor_distance(GPIO_ECHO_TOP)
    middle_distance = sensor_distance(GPIO_ECHO_MIDDLE)
    bottom_distance = sensor_distance(GPIO_ECHO_BOTTOM)
    
    return {
            "top":top_distance, 
            "middle": middle_distance, 
            "bottom":bottom_distance
            }


def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy() == True:
        continue


if __name__ == "__main__":
    pygame.init()

    try:
        while True:
            dist = distance()
            print ("Measured Distances =",dist)
            time.sleep(1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
