import RPi.GPIO as GPIO
import time

GPIO.cleanup() #清空所有引脚状态 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(3,GPIO.OUT)

GPIO.output(3,False)

pwm=GPIO.PWM(5,500)
pwm.start(0)
timeStart=time.time()
try:
	while 1:
		for dc in range(80, 100, 1):
			pwm.ChangeDutyCycle(dc)
			print(dc)
			time.sleep(0.1)
		for dc in range(100, 79, -1):
			pwm.ChangeDutyCycle(dc)
			time.sleep(0.1)
except KeyboardInterrupt:
	pass
		
pwm.ChangeDutyCycle(50)
pwm.stop()

GPIO.cleanup() #清空所有引脚状态 
#GPIO.cleanup(chanList) #清空部分引脚状态