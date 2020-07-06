import argparse 
import logging 
import time
from RPi import GPIO
from rpi_rf import RFDevice 

def rx_callback(inV):
  print("rsCallback",inV)

rfRX = RFDevice(27)
rfRX.enable_rx()
timestamp = None
#GPIO.add_event_detect(17, GPIO.BOTH)
GPIO.add_event_callback(27, rx_callback)

while True:
    if rfRX.rx_code_timestamp != timestamp:
        timestamp = rfRX.rx_code_timestamp
        logging.info("RX:::"+str(rfRX.rx_code) +
                     " [pulselength " + str(rfRX.rx_pulselength) +
                     ", protocol " + str(rfRX.rx_proto) + "]")
    time.sleep(0.01)
    #print("waiting..",rfRX.rx_code_timestamp)

rfRX.cleanup()

