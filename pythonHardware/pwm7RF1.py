import RPi.GPIO as GPIO
import time
BRIGHT = 128#128          #brightest value
BREATH_LOW = 8#78
BREATH_HIGH=128#128
DARK=0            #Darkest valule

state=2 #state 0 关，1开,2,呼吸,3,保持
dc = DARK#存储最新数值变数，我们将使用它来从上到下计数
dcTarget = DARK
rate=0.1#0.01
rateClose=0.1#0.01
breath=1.1


#callback for myThread
def ledCallback(inPWM):
	global dc
	global dcTarget
	global rateClose
	global BRIGHT
	if(abs(dcTarget-dc) >= 1):
		if (dcTarget<dc): dc+=(dcTarget-dc)*rateClose
		else : dc+=(dcTarget-dc)*rate
		#analogWrite(LED,int(dc))
		print('after ledCallback',dcTarget,dc,round(dc*100/255))
		inPWM.ChangeDutyCycle(round(dc*100/255))
		
	else:
		dc=dcTarget


def statControl():
	global state
	global BRIGHT
	global dc
	global dcTarget
	global BREATH_HIGH
	global breath
	#bn=digitalRead(BN);
	#digitalWrite(LED_INFO,state-1);
	#if(state!=2 || (state==2 && bn==0)):state=bn
	if(state==1):#开灯
		if(BRIGHT==dc):#已经开灯完成
			state=2
		else:
			dcTarget=BRIGHT
	
	if(state==0):#关灯
		dcTarget=DARK
	
	if(state==2):#呼吸灯
		#if(dcTarget>BREATH_LOW and dcTarget<BREATH_HIGH):
		#	dcTarget+=breath
		if(dcTarget<=BREATH_LOW or dcTarget>=BREATH_HIGH):
			if dcTarget<=BREATH_LOW : 
				dcTarget = BREATH_LOW
				breath=abs(breath)
			if dcTarget>=BREATH_HIGH : 
				dcTarget = BREATH_HIGH
				breath=-abs(breath)
		#print('after statControl',dcTarget,breath,dcTarget+breath)
		dcTarget+=breath

pLED0=18
pLED1=16
#GPIO.cleanup() #清空所有引脚状态 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pLED0,GPIO.OUT)
GPIO.setup(pLED1,GPIO.OUT)
#GPIO.setup(1,GPIO.OUT)

#GPIO.output(3,False)

pwm=GPIO.PWM(pLED0,1000)
pwm.start(0)

pwm1=GPIO.PWM(pLED1,1000)
pwm1.start(0)
timeStart=time.time()
try:
	'''
	while 1:
		pwm.ChangeDutyCycle(50)
		continue
		for dc in range(0, 100, 1):
			pwm.ChangeDutyCycle(dc)
			print(dc)
			time.sleep(0.03)
		for dc in range(100, 0, -1):
			pwm.ChangeDutyCycle(dc)
			print(dc)
			time.sleep(0.03)
	
	'''
	while 1:
		statControl()
		#if(myTimer.isTimeReached(now)):#/check if execution time has been reached
		ledCallback(pwm)
		ledCallback(pwm1)
		time.sleep(0.1)
	
except KeyboardInterrupt:
	pass
		
pwm.ChangeDutyCycle(0)
pwm.stop()

GPIO.cleanup() #清空所有引脚状态 
#GPIO.cleanup(chanList) #清空部分引脚状态