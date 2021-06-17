import argparse
import signal
import sys
import time
import logging


from functions import sendMore, getData
from rpi_rf import RFDevice

rfdevice = None


light_args=[{'wrgb':[4095,2000,500,0]},
    {'toggle':1},
    {'wrgb':[0,4095,800,0]},
    {'wrgb':[0,156,30,0]},
    ]

def exithandler(signal, frame):
    rfdevice.cleanup()
    sys.exit(0)

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

parser = argparse.ArgumentParser(description='Receives a decimal code via a 433/315MHz GPIO device')
parser.add_argument('-g', dest='gpio', type=int, default=27,
                    help="GPIO pin (Default: 27)")
args = parser.parse_args()

signal.signal(signal.SIGINT, exithandler)
rfdevice = RFDevice(args.gpio)
rfdevice.enable_rx()
timestamp = None
logging.info("Listening for codes on GPIO " + str(args.gpio))
#print('Listening')
while True:
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        code=str(rfdevice.rx_code)
        print(code)
        if code[:2]==code[-2:]=='69':
            num=int(code[2:-2])
            print('{}: {}'.format(num,light_args[num]))
            sendMore(**light_args[num])
        logging.info(str(rfdevice.rx_code) +
                     " [pulselength " + str(rfdevice.rx_pulselength) +
                     ", protocol " + str(rfdevice.rx_proto) + "]")
#        print(str(rfdevice.rx_code) +
#                     " [pulselength " + str(rfdevice.rx_pulselength) +
#                     ", protocol " + str(rfdevice.rx_proto) + "]")
    time.sleep(0.05)
rfdevice.cleanup()
