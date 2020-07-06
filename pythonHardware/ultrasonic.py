
#Libraries
import RPi.GPIO as GPIO
import time

class GPIO_Ultrasonic:
	GPIO_TRIGGER = 29
	GPIO_ECHO = 31
	#set GPIO Pins
	def __init__(pTrigger,pEcho):
		GPIO_Ultrasonic.
	 
	def distance():
		# set Trigger to HIGH
		GPIO.output(GPIO_TRIGGER, True)
	 
		# set Trigger after 0.01ms to LOW
		time.sleep(0.00001)
		GPIO.output(GPIO_TRIGGER, False)
	 
		StartTime = time.time()
		StopTime = time.time()
	 
		# save StartTime
		while GPIO.input(GPIO_ECHO) == 0:
			StartTime = time.time()
	 
		# save time of arrival
		while GPIO.input(GPIO_ECHO) == 1:
			StopTime = time.time()
	 
		# time difference between start and arrival
		TimeElapsed = StopTime - StartTime
		# multiply with the sonic speed (34300 cm/s)
		# and divide by 2, because there and back
		distance = (TimeElapsed * 34300) / 2
	 
		return distance

	def mapCut(inV,inMin,inMax,mapRang=1):
		v=inV
		if inV<inMin :v=inMin
		if inV>inMax : v=inMax
		res=(v-inMin)/(inMax-inMin)
		return res*mapRang

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist,mapCut(dist,10,40))
            time.sleep(.1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()