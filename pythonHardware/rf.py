import argparse 
import logging 
import time
from rpi_rf import RFDevice 
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s',) 
parser = argparse.ArgumentParser(description='Sends a decimal code via a 433/315MHz GPIO device') 
parser.add_argument('code', metavar='CODE', type=int,
                    help="Decimal code to send") 
parser.add_argument('-g', dest='gpio', type=int, default=18,
                    help="GPIO pin (Default: 18)") 
parser.add_argument('-p', dest='pulselength', type=int, default=None,
                    help="Pulselength (Default: 350)") 
parser.add_argument('-t', dest='protocol', type=int, default=None,
                    help="Protocol (Default: 1)") 
args = parser.parse_args() 
rfdevice = RFDevice(args.gpio) 
rfdevice.enable_tx() 

rfRX = RFDevice(23)
rfRX.enable_rx()
timestamp = None

if args.protocol:
    protocol = args.protocol 
else:
    protocol = "default" 
if args.pulselength:
    pulselength = args.pulselength 
else:
    pulselength = "default" 
logging.info(str(args.code) +
             " [protocol: " + str(protocol) +
             ", pulselength: " + str(pulselength) + "]") 
rfdevice.tx_code(args.code, args.protocol, args.pulselength)
#rfdevice.cleanup()

while True:
    if rfRX.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        logging.info("RX:::"+str(rfdevice.rx_code) +
                     " [pulselength " + str(rfdevice.rx_pulselength) +
                     ", protocol " + str(rfdevice.rx_proto) + "]")
    time.sleep(0.01)
    rfdevice.tx_code(args.code, args.protocol, args.pulselength)
    print("sended..")
rfRX.cleanup()
rfdevice.cleanup()
